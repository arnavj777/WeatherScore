import pandas as pd
import numpy as np
import os
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import xgboost as xgb
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import warnings
warnings.filterwarnings('ignore')

# Define zones and their airports
ZONES = {
    'Northeast': ['BOS', 'JFK'],
    'PacificCoast': ['LAX', 'SEA'],
    'RockyMountains': ['DEN'],
    'CentralPlains': ['ORD', 'OKC'],
    'Southeast': ['ATL', 'MIA']
}

def load_flight_delays(filepath):
    """Load and process flight delay data"""
    print("\nLoading flight delay data...")
    
    df = pd.read_csv(filepath, low_memory=False)
    print(f"Loaded {len(df):,} delay records")
    
    # Parse date
    df['FL_DATE'] = pd.to_datetime(df['FL_DATE'])
    df['date'] = df['FL_DATE'].dt.date
    
    # Extract hour from CRS_DEP_TIME
    def parse_time(time_val):
        try:
            time_str = str(int(float(time_val)))
            if len(time_str) <= 2:
                hour = int(time_str)
            else:
                hour = int(time_str[:-2])
            return hour % 24
        except:
            return 12  # Default noon
    
    df['departure_hour'] = df['CRS_DEP_TIME'].apply(parse_time)
    
    # Calculate total delay (use weather delay or total delay)
    df['total_delay'] = df['DEP_DELAY'].fillna(0)
    df['weather_delay'] = df['WEATHER_DELAY'].fillna(0)
    
    # Create a delay indicator (1 if delay > 15 minutes, else 0)
    df['has_delay'] = (df['total_delay'] > 15).astype(int)
    
    # Create delay severity score (0-100 based on delay minutes)
    df['delay_score'] = np.clip(df['total_delay'] / 4, 0, 100)  # 4 hours = 100
    
    print(f"Delay data summary:")
    print(f"  Records: {len(df):,}")
    print(f"  Airports: {sorted(df['ORIGIN'].unique())}")
    print(f"  Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"  Average delay: {df['total_delay'].mean():.1f} minutes")
    
    return df[['ORIGIN', 'date', 'departure_hour', 'total_delay', 'weather_delay', 
               'has_delay', 'delay_score']]

def combine_weather_delays(weather_df, delay_df):
    """Combine weather data with flight delay data"""
    print("\nCombining weather and delay data...")
    
    # Merge on airport and date
    combined = pd.merge(
        delay_df,
        weather_df,
        left_on=['ORIGIN', 'date'],
        right_on=['airport', 'date'],
        how='inner'
    )
    
    print(f"Combined records: {len(combined):,}")
    print(f"Matching rate: {len(combined)/len(delay_df)*100:.1f}%")
    
    return combined

def prepare_features(combined_df):
    """Prepare features for modeling"""
    print("\nPreparing features...")
    
    # Select feature columns
    feature_columns = [
        'temperature_c', 'dewpoint_c', 'wind_direction', 'wind_speed_kts',
        'visibility_km', 'ceiling_ft', 'sea_level_pressure_mb',
        'gust', 'relh', 'temp_spread', 'gust_factor', 'ceiling_vis_ratio',
        'pressure_change', 'humidity', 'hour', 'month', 'is_night',
        'departure_hour'
    ]
    
    # Filter to available columns
    available_features = [col for col in feature_columns if col in combined_df.columns]
    
    X = combined_df[available_features].copy()
    y = combined_df['delay_score'].copy()
    
    # Handle missing values
    X = X.fillna(X.median())
    X = X.replace([np.inf, -np.inf], np.nan).fillna(X.median())
    
    print(f"Features: {len(available_features)}")
    print(f"Records: {len(X):,}")
    print(f"Target range: {y.min():.1f} to {y.max():.1f}")
    
    return X, y, available_features

def train_zone_model(zone_name, X, y, features, output_dir='models/zones'):
    """Train XGBoost model for a specific zone"""
    print(f"\n{'='*60}")
    print(f"Training Model for {zone_name}")
    print(f"{'='*60}")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"Training set: {X_train.shape[0]:,}")
    print(f"Test set: {X_test.shape[0]:,}")
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train model
    print("\nTraining XGBoost model...")
    model = xgb.XGBRegressor(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.1,
        min_child_weight=3,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train_scaled, y_train)
    
    # Make predictions
    y_train_pred = model.predict(X_train_scaled)
    y_test_pred = model.predict(X_test_scaled)
    
    # Evaluate
    train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
    test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
    train_mae = mean_absolute_error(y_train, y_train_pred)
    test_mae = mean_absolute_error(y_test, y_test_pred)
    train_r2 = r2_score(y_train, y_train_pred)
    test_r2 = r2_score(y_test, y_test_pred)
    
    print(f"\n{'='*60}")
    print(f"MODEL EVALUATION - {zone_name}")
    print(f"{'='*60}")
    print(f"\nTraining:")
    print(f"  RMSE: {train_rmse:.2f}")
    print(f"  MAE: {train_mae:.2f}")
    print(f"  R²: {train_r2:.3f}")
    print(f"\nTest:")
    print(f"  RMSE: {test_rmse:.2f}")
    print(f"  MAE: {test_mae:.2f}")
    print(f"  R²: {test_r2:.3f}")
    
    # Feature importance
    print(f"\nTop 5 Features:")
    feature_importance = pd.DataFrame({
        'feature': features,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    for i, row in feature_importance.head(5).iterrows():
        print(f"  {row['feature']}: {row['importance']:.3f}")
    
    # Save model
    model_path = os.path.join(output_dir, f'{zone_name}_model.pkl')
    scaler_path = os.path.join(output_dir, f'{zone_name}_scaler.pkl')
    features_path = os.path.join(output_dir, f'{zone_name}_features.txt')
    
    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)
    
    with open(features_path, 'w') as f:
        for name in features:
            f.write(name + '\n')
    
    print(f"\n✅ Model saved to {model_path}")
    print(f"✅ Scaler saved to {scaler_path}")
    print(f"✅ Features saved to {features_path}")
    
    return {
        'model': model,
        'scaler': scaler,
        'features': features,
        'train_rmse': train_rmse,
        'test_rmse': test_rmse,
        'train_r2': train_r2,
        'test_r2': test_r2
    }

def main():
    print("="*60)
    print("MULTI-ZONE FLIGHT RISK MODEL TRAINING")
    print("="*60)
    
    # Load delay data
    delay_df = load_flight_delays('Data/T_ONTIME_REPORTING.csv')
    
    # Train models for each zone
    results = {}
    
    for zone_name in ZONES.keys():
        # Load weather data
        weather_path = f'Data/processed_zones/{zone_name}_weather.csv'
        
        if not os.path.exists(weather_path):
            print(f"\n⚠️  Skipping {zone_name}: weather data not found")
            continue
        
        print(f"\n{'='*60}")
        print(f"Processing {zone_name}")
        print(f"{'='*60}")
        
        weather_df = pd.read_csv(weather_path, parse_dates=['valid'])
        weather_df['date'] = pd.to_datetime(weather_df['valid']).dt.date
        
        # Get airports for this zone
        airports = ZONES[zone_name]
        
        # Filter delay data for this zone's airports
        zone_delay = delay_df[delay_df['ORIGIN'].isin(airports)].copy()
        
        if len(zone_delay) == 0:
            print(f"⚠️  No delay data for {zone_name} airports")
            continue
        
        # Combine weather and delay data
        combined = combine_weather_delays(weather_df, zone_delay)
        
        if len(combined) == 0:
            print(f"⚠️  No matching weather-delay records for {zone_name}")
            continue
        
        # Prepare features
        X, y, features = prepare_features(combined)
        
        # Train model
        result = train_zone_model(zone_name, X, y, features)
        results[zone_name] = result
    
    # Summary
    print("\n" + "="*60)
    print("TRAINING SUMMARY")
    print("="*60)
    
    for zone_name, result in results.items():
        print(f"\n{zone_name}:")
        print(f"  Train R²: {result['train_r2']:.3f}")
        print(f"  Test R²: {result['test_r2']:.3f}")
        print(f"  Test RMSE: {result['test_rmse']:.2f}")
    
    print(f"\n✅ Trained {len(results)} zone models successfully!")
    print(f"\nModels saved in: models/zones/")

if __name__ == "__main__":
    main()
