"""
Train PacificCoast Region Flight Risk Model
"""
import pandas as pd
import numpy as np
import os
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import VarianceThreshold
import xgboost as xgb
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import warnings
warnings.filterwarnings('ignore')

# PacificCoast airports from Excel file
PACIFICCOAST_AIRPORTS = ['LAX', 'SFO', 'SEA', 'PDX', 'SAN', 'OAK', 'SJC', 'SMF']
ZONE_NAME = 'PacificCoast'

def load_flight_delays(filepath):
    """Load and process flight delay data"""
    print("\nLoading flight delay data...")
    
    df = pd.read_csv(filepath, low_memory=False)
    print(f"Loaded {len(df):,} delay records")
    
    df['FL_DATE'] = pd.to_datetime(df['FL_DATE'])
    df['date'] = df['FL_DATE'].dt.date
    
    def parse_time(time_val):
        try:
            time_str = str(int(float(time_val)))
            if len(time_str) <= 2:
                hour = int(time_str)
            else:
                hour = int(time_str[:-2])
            return hour % 24
        except:
            return 12
    
    df['departure_hour'] = df['CRS_DEP_TIME'].apply(parse_time)
    df['total_delay'] = df['DEP_DELAY'].fillna(0)
    df['weather_delay'] = df['WEATHER_DELAY'].fillna(0)
    
    df['delay_score'] = np.where(
        df['weather_delay'] > 0,
        np.clip(df['weather_delay'] / 6, 0, 100),
        np.where(
            df['total_delay'] > 15,
            np.clip(df['total_delay'] / 8, 0, 50),
            0
        )
    )
    
    df_filtered = df[
        (df['total_delay'] > 10) | (df['weather_delay'] > 0) | (df['total_delay'] < -5)
    ].copy()
    
    print(f"Filtered to {len(df_filtered):,} records")
    return df_filtered[['ORIGIN', 'date', 'departure_hour', 'delay_score']]

def prepare_zone_data():
    """Load and prepare PacificCoast zone data"""
    print("="*60)
    print(f"TRAINING {ZONE_NAME} MODEL")
    print("="*60)
    
    delay_df = load_flight_delays('Data/T_ONTIME_REPORTING.csv')
    zone_delays = delay_df[delay_df['ORIGIN'].isin(PACIFICCOAST_AIRPORTS)].copy()
    print(f"PacificCoast delay records: {len(zone_delays):,}")
    
    weather_path = 'Data/processed_zones/PacificCoast_weather.csv'
    if not os.path.exists(weather_path):
        print(f"Error: {weather_path} not found. Run process_all_zones.py first.")
        return None
    
    weather_df = pd.read_csv(weather_path, parse_dates=['valid'])
    weather_df['date'] = pd.to_datetime(weather_df['valid']).dt.date
    
    combined = pd.merge(
        zone_delays,
        weather_df,
        left_on=['ORIGIN', 'date'],
        right_on=['airport', 'date'],
        how='inner'
    )
    
    print(f"Combined records: {len(combined):,}")
    
    feature_columns = [
        'temperature_c', 'dewpoint_c', 'wind_direction', 'wind_speed_kts',
        'visibility_km', 'ceiling_ft', 'sea_level_pressure_mb',
        'gust', 'relh', 'temp_spread', 'gust_factor', 'ceiling_vis_ratio',
        'pressure_change', 'humidity', 'hour', 'month', 'is_night',
        'departure_hour'
    ]
    
    available_features = [col for col in feature_columns if col in combined.columns]
    X = combined[available_features].copy()
    y = combined['delay_score'].copy()
    
    X = X.fillna(X.median())
    X = X.replace([np.inf, -np.inf], np.nan).fillna(X.median())
    
    selector = VarianceThreshold(threshold=0.01)
    X_selected = selector.fit_transform(X)
    selected_features = [available_features[i] for i in range(len(available_features)) if selector.variances_[i] > 0.01]
    X = pd.DataFrame(X_selected, columns=selected_features, index=X.index)
    
    print(f"Final features: {len(selected_features)}")
    return X, y, selected_features

def train_model(X, y, features):
    """Train the XGBoost model"""
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print(f"Training samples: {len(X_train):,}")
    print(f"Test samples: {len(X_test):,}")
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print("\nTraining XGBoost model...")
    model = xgb.XGBRegressor(
        n_estimators=300, max_depth=8, learning_rate=0.05,
        min_child_weight=2, subsample=0.9, colsample_bytree=0.9, gamma=0.1,
        random_state=42, n_jobs=-1
    )
    
    model.fit(X_train_scaled, y_train)
    
    y_train_pred = model.predict(X_train_scaled)
    y_test_pred = model.predict(X_test_scaled)
    
    train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
    test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
    train_mae = mean_absolute_error(y_train, y_train_pred)
    test_mae = mean_absolute_error(y_test, y_test_pred)
    train_r2 = r2_score(y_train, y_train_pred)
    test_r2 = r2_score(y_test, y_test_pred)
    
    print("\n" + "="*60)
    print("MODEL EVALUATION")
    print("="*60)
    print(f"\nTrain R²: {train_r2:.3f}, RMSE: {train_rmse:.2f}, MAE: {train_mae:.2f}")
    print(f"Test R²:  {test_r2:.3f}, RMSE: {test_rmse:.2f}, MAE: {test_mae:.2f}")
    
    print("\nTop 5 Features:")
    feature_importance = pd.DataFrame({
        'feature': features,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    for i, row in feature_importance.head(5).iterrows():
        print(f"  {row['feature']}: {row['importance']:.3f}")
    
    return model, scaler, features

def save_model(model, scaler, features):
    """Save trained model"""
    os.makedirs('models/zones', exist_ok=True)
    
    model_path = f'models/zones/{ZONE_NAME}_model.pkl'
    scaler_path = f'models/zones/{ZONE_NAME}_scaler.pkl'
    features_path = f'models/zones/{ZONE_NAME}_features.txt'
    
    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)
    
    with open(features_path, 'w') as f:
        for name in features:
            f.write(name + '\n')
    
    print(f"\n✅ Model saved to {model_path}")

def main():
    result = prepare_zone_data()
    if result is None:
        return
    
    X, y, features = result
    model, scaler, features = train_model(X, y, features)
    save_model(model, scaler, features)
    
    print(f"\n✅ {ZONE_NAME} model training complete!")

if __name__ == "__main__":
    main()
