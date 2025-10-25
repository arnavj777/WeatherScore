"""
Zone-based flight risk prediction system
Predicts flight risk using region-specific trained models
"""

import pandas as pd
import numpy as np
import joblib
import os

ZONES = {
    'Northeast': ['BOS', 'JFK'],
    'PacificCoast': ['LAX', 'SEA'],
    'RockyMountains': ['DEN'],
    'CentralPlains': ['ORD', 'OKC'],
    'Southeast': ['ATL', 'MIA']
}

def load_zone_model(zone_name):
    """Load model files for a specific zone"""
    model_dir = 'models/zones'
    
    model_path = os.path.join(model_dir, f'{zone_name}_model.pkl')
    scaler_path = os.path.join(model_dir, f'{zone_name}_scaler.pkl')
    features_path = os.path.join(model_dir, f'{zone_name}_features.txt')
    
    if not all(os.path.exists(p) for p in [model_path, scaler_path, features_path]):
        raise FileNotFoundError(f"Model files not found for {zone_name}")
    
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    
    with open(features_path, 'r') as f:
        features = [line.strip() for line in f.readlines()]
    
    return model, scaler, features

def prepare_features(weather_data, feature_names):
    """Prepare features for prediction"""
    df = pd.DataFrame([weather_data]) if isinstance(weather_data, dict) else weather_data.copy()
    
    # Ensure all required features exist
    for feature in feature_names:
        if feature not in df.columns:
            raise ValueError(f"Missing required feature: {feature}")
    
    X = df[feature_names].copy()
    
    # Handle missing values
    X = X.fillna(X.median())
    X = X.replace([np.inf, -np.inf], np.nan).fillna(X.median())
    
    return X

def predict_zone_risk(zone_name, weather_data):
    """
    Predict flight risk for a specific zone
    
    Parameters:
    -----------
    zone_name : str
        Zone name (e.g., 'Northeast', 'PacificCoast', etc.)
    weather_data : dict or pd.DataFrame
        Weather conditions with required features
    
    Returns:
    --------
    float or np.array
        Risk score(s) between 0-100 (100 = maximum risk)
    """
    # Load zone model
    model, scaler, features = load_zone_model(zone_name)
    
    # Prepare features
    X = prepare_features(weather_data, features)
    
    # Scale features
    X_scaled = scaler.transform(X)
    
    # Make predictions
    predictions = model.predict(X_scaled)
    
    # Clip to 0-100 range
    predictions = np.clip(predictions, 0, 100)
    
    return predictions

def interpret_risk_score(score):
    """Interpret the risk score"""
    if score < 20:
        return "Very Low Risk"
    elif score < 40:
        return "Low Risk"
    elif score < 60:
        return "Moderate Risk"
    elif score < 80:
        return "High Risk"
    else:
        return "Very High Risk"

def predict_all_zones(weather_data):
    """
    Predict risk for all zones and compare
    
    Parameters:
    -----------
    weather_data : dict
        Weather conditions (will be applied to all zones)
    
    Returns:
    --------
    dict
        Predictions for each zone
    """
    results = {}
    
    for zone_name in ZONES.keys():
        try:
            risk_score = predict_zone_risk(zone_name, weather_data)
            results[zone_name] = {
                'score': risk_score[0],
                'category': interpret_risk_score(risk_score[0])
            }
        except Exception as e:
            print(f"Error predicting for {zone_name}: {e}")
            results[zone_name] = None
    
    return results

def example_usage():
    """Example of how to use the zone-based prediction system"""
    
    # Example weather for Northeast
    northeast_weather = {
        'temperature_c': 5.0,
        'dewpoint_c': 2.0,
        'wind_direction': 270,
        'wind_speed_kts': 15.0,
        'visibility_km': 8.0,
        'ceiling_ft': 2500.0,
        'sea_level_pressure_mb': 1015.0,
        'gust': 20.0,
        'relh': 75.0,
        'temp_spread': 3.0,
        'gust_factor': 1.33,
        'ceiling_vis_ratio': 0.95,
        'pressure_change': -1.0,
        'humidity': 75.0,
        'hour': 14,
        'month': 1,
        'is_night': 0,
        'departure_hour': 14
    }
    
    print("="*60)
    print("ZONE-BASED FLIGHT RISK PREDICTION")
    print("="*60)
    
    # Predict for Northeast
    print("\nPredicting for Northeast...")
    risk = predict_zone_risk('Northeast', northeast_weather)
    category = interpret_risk_score(risk[0])
    print(f"Risk Score: {risk[0]:.1f}/100")
    print(f"Category: {category}")
    
    # Predict for all zones
    print("\n" + "="*60)
    print("Comparing All Zones")
    print("="*60)
    
    all_results = predict_all_zones(northeast_weather)
    
    for zone, result in all_results.items():
        if result:
            print(f"\n{zone}:")
            print(f"  Score: {result['score']:.1f}/100")
            print(f"  Category: {result['category']}")

if __name__ == "__main__":
    example_usage()
