import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import xgboost as xgb
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import warnings
warnings.filterwarnings('ignore')

def create_flight_risk_score(data):
    """
    Create a flight risk score based on weather conditions.
    Higher score = higher risk.
    
    Risk factors:
    - Low visibility (<1 mile = 100, >10 miles = 0)
    - Low ceiling (<200 ft = 100, >3000 ft = 0)
    - High winds (>40 kts = 100, <10 kts = 0)
    - Poor weather conditions (precipitation, storms, etc.)
    - Temperature extremes
    - Icing conditions
    """
    score = np.zeros(len(data))
    
    # Visibility score (lower visibility = higher risk)
    vis = data['visibility_km_aus'].fillna(10)  # Default to good visibility
    score += np.clip((10 - vis) / 9 * 40, 0, 40)  # 0-40 points
    
    # Ceiling score (lower ceiling = higher risk)
    ceiling = data['ceiling_ft_aus'].fillna(5000)
    score += np.clip((3000 - ceiling) / 28 * 30, 0, 30)  # 0-30 points
    
    # Wind speed score (higher winds = higher risk)
    wind = data['wind_speed_kts_aus'].fillna(0)
    score += np.clip((wind - 10) / 3 * 20, 0, 20)  # 0-20 points
    
    # Gust score (strong gusts = higher risk)
    gust = data['gust'].fillna(0)
    score += np.clip((gust - 20) / 2 * 10, 0, 10)  # 0-10 points
    
    # Clip to 0-100 range
    score = np.clip(score, 0, 100)
    
    return score

def engineer_features(data):
    """Create additional features for the model"""
    df = data.copy()
    
    # Temperature spread (difference between temp and dewpoint)
    df['temp_spread'] = df['temperature_c_aus'] - df['dewpoint_c_aus']
    
    # Wind gust factor (gust / wind speed ratio)
    df['gust_factor'] = df['gust'] / (df['wind_speed_kts_aus'] + 1)
    
    # Ceiling to visibility ratio
    df['ceiling_vis_ratio'] = df['ceiling_ft_aus'] / (df['visibility_km_aus'] * 1000 / 3.28084 + 1)
    
    # Pressure change indicator
    df['pressure_change'] = df['sea_level_pressure_mb_aus'].diff().fillna(0)
    
    # Humidity (from temp and dewpoint)
    df['humidity'] = df['relh'].fillna(50)
    
    # Time features
    if 'valid' in df.columns:
        df['hour'] = pd.to_datetime(df['valid']).dt.hour
        df['month'] = pd.to_datetime(df['valid']).dt.month
        df['is_night'] = ((df['hour'] >= 20) | (df['hour'] <= 6)).astype(int)
    
    return df

def prepare_model_data(data):
    """Prepare data for modeling"""
    print("\nPreparing model data...")
    
    # Create risk score
    data['risk_score'] = create_flight_risk_score(data)
    
    print(f"Risk score statistics:")
    print(data['risk_score'].describe())
    
    # Engineer features
    data = engineer_features(data)
    
    # Select features for modeling
    feature_columns = [
        'temperature_c_aus', 'dewpoint_c_aus', 'wind_direction_aus', 'wind_speed_kts_aus',
        'visibility_km_aus', 'ceiling_ft_aus', 'sea_level_pressure_mb_aus',
        'gust', 'relh', 'temp_spread', 'gust_factor', 'ceiling_vis_ratio',
        'pressure_change', 'humidity'
    ]
    
    # Add time features if available
    if 'hour' in data.columns:
        feature_columns.extend(['hour', 'month', 'is_night'])
    
    # Filter to available columns
    available_features = [col for col in feature_columns if col in data.columns]
    
    print(f"\nUsing {len(available_features)} features for modeling")
    print(f"Features: {available_features}")
    
    # Prepare feature matrix
    X = data[available_features].copy()
    y = data['risk_score'].copy()
    
    # Handle missing values
    X = X.fillna(X.median())
    
    # Remove any infinite values
    X = X.replace([np.inf, -np.inf], np.nan).fillna(X.median())
    
    print(f"\nFeature matrix shape: {X.shape}")
    print(f"Target shape: {y.shape}")
    print(f"\nMissing values in features: {X.isnull().sum().sum()}")
    
    return X, y, available_features

def train_model(X, y, available_features):
    """Train XGBoost model"""
    print("\n" + "="*60)
    print("TRAINING XGBOOST MODEL")
    print("="*60)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"\nTraining set: {X_train.shape}")
    print(f"Test set: {X_test.shape}")
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train XGBoost model
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
    
    # Evaluate model
    print("\n" + "="*60)
    print("MODEL EVALUATION")
    print("="*60)
    
    train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
    test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
    train_mae = mean_absolute_error(y_train, y_train_pred)
    test_mae = mean_absolute_error(y_test, y_test_pred)
    train_r2 = r2_score(y_train, y_train_pred)
    test_r2 = r2_score(y_test, y_test_pred)
    
    print(f"\nTraining Set:")
    print(f"  RMSE: {train_rmse:.2f}")
    print(f"  MAE: {train_mae:.2f}")
    print(f"  R²: {train_r2:.3f}")
    
    print(f"\nTest Set:")
    print(f"  RMSE: {test_rmse:.2f}")
    print(f"  MAE: {test_mae:.2f}")
    print(f"  R²: {test_r2:.3f}")
    
    # Feature importance
    print("\n" + "="*60)
    print("FEATURE IMPORTANCE (Top 10)")
    print("="*60)
    feature_importance = pd.DataFrame({
        'feature': available_features,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print(feature_importance.head(10).to_string(index=False))
    
    return model, scaler, available_features, X_test, y_test, y_test_pred

def save_model(model, scaler, feature_names, save_dir='models'):
    """Save the trained model"""
    import os
    import joblib
    
    # Create directory if it doesn't exist
    os.makedirs(save_dir, exist_ok=True)
    
    # Save model and scaler
    model_path = os.path.join(save_dir, 'xgboost_flight_risk_model.pkl')
    scaler_path = os.path.join(save_dir, 'scaler.pkl')
    features_path = os.path.join(save_dir, 'feature_names.txt')
    
    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)
    
    with open(features_path, 'w') as f:
        for name in feature_names:
            f.write(name + '\n')
    
    print(f"\nModel saved to {model_path}")
    print(f"Scaler saved to {scaler_path}")
    print(f"Feature names saved to {features_path}")

if __name__ == "__main__":
    print("="*60)
    print("FLIGHT RISK SCORING MODEL TRAINING")
    print("="*60)
    
    # Load cleaned data
    print("\nLoading cleaned weather data...")
    data = pd.read_csv('Data/cleaned_weather_data.csv')
    print(f"Data shape: {data.shape}")
    
    # Prepare model data
    X, y, feature_names = prepare_model_data(data)
    
    # Train model
    model, scaler, feature_names, X_test, y_test, y_test_pred = train_model(X, y, feature_names)
    
    # Save model
    save_model(model, scaler, feature_names)
    
    print("\n" + "="*60)
    print("MODEL TRAINING COMPLETE")
    print("="*60)
    print("\nThe model is now ready to predict flight risk scores (0-100)")
    print("where 100 represents maximum flight risk and 0 represents minimal risk.")
