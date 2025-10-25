import pandas as pd
import numpy as np
import joblib
import os

def load_model():
    """Load the trained model and scaler"""
    model_path = 'models/xgboost_flight_risk_model.pkl'
    scaler_path = 'models/scaler.pkl'
    features_path = 'models/feature_names.txt'
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found at {model_path}. Please train the model first.")
    
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    
    with open(features_path, 'r') as f:
        feature_names = [line.strip() for line in f.readlines()]
    
    return model, scaler, feature_names

def prepare_features(data, feature_names):
    """Prepare features for prediction"""
    df = data.copy()
    
    # Ensure all required features exist
    for feature in feature_names:
        if feature not in df.columns:
            raise ValueError(f"Missing required feature: {feature}")
    
    # Extract features in the correct order
    X = df[feature_names].copy()
    
    # Handle missing values
    X = X.fillna(X.median())
    
    # Remove any infinite values
    X = X.replace([np.inf, -np.inf], np.nan).fillna(X.median())
    
    return X

def predict_risk(weather_data):
    """
    Predict flight risk score for given weather conditions.
    
    Parameters:
    -----------
    weather_data : dict or pd.DataFrame
        Weather conditions with required features
    
    Returns:
    --------
    float or np.array
        Risk score(s) between 0-100 (100 = maximum risk)
    """
    # Load model
    model, scaler, feature_names = load_model()
    
    # Convert dict to DataFrame if needed
    if isinstance(weather_data, dict):
        df = pd.DataFrame([weather_data])
    else:
        df = weather_data.copy()
    
    # Prepare features
    X = prepare_features(df, feature_names)
    
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

def predict_from_file(file_path):
    """Predict risk scores for a CSV file of weather data"""
    # Load data
    data = pd.read_csv(file_path)
    
    # Make predictions
    predictions = predict_risk(data)
    
    # Add predictions to dataframe
    data['risk_score'] = predictions
    data['risk_category'] = [interpret_risk_score(s) for s in predictions]
    
    return data

if __name__ == "__main__":
    print("="*60)
    print("FLIGHT RISK PREDICTION")
    print("="*60)
    
    # Example usage with a sample
    print("\nExample: Predicting risk for sample weather conditions")
    
    sample_weather = {
        'temperature_c_aus': 15.0,
        'dewpoint_c_aus': 10.0,
        'wind_direction_aus': 270,
        'wind_speed_kts_aus': 5.0,
        'visibility_km_aus': 10.0,
        'ceiling_ft_aus': 5000.0,
        'sea_level_pressure_mb_aus': 1013.0,
        'gust': 0.0,
        'relh': 70.0,
        'temp_spread': 5.0,
        'gust_factor': 0.0,
        'ceiling_vis_ratio': 1.5,
        'pressure_change': 0.0,
        'humidity': 70.0,
        'hour': 12,
        'month': 6,
        'is_night': 0
    }
    
    print("\nWeather Conditions:")
    print(f"  Temperature: {sample_weather['temperature_c_aus']}°C")
    print(f"  Wind Speed: {sample_weather['wind_speed_kts_aus']} knots")
    print(f"  Visibility: {sample_weather['visibility_km_aus']} km")
    print(f"  Ceiling: {sample_weather['ceiling_ft_aus']} ft")
    
    risk_score = predict_risk(sample_weather)
    risk_category = interpret_risk_score(risk_score[0])
    
    print(f"\nPredicted Risk Score: {risk_score[0]:.1f}/100")
    print(f"Risk Category: {risk_category}")
    
    # Example with poor weather
    print("\n" + "-"*60)
    print("Example: Predicting risk for poor weather conditions")
    
    poor_weather = sample_weather.copy()
    poor_weather['visibility_km_aus'] = 0.5  # Poor visibility
    poor_weather['ceiling_ft_aus'] = 200.0   # Low ceiling
    poor_weather['wind_speed_kts_aus'] = 35.0  # Strong winds
    poor_weather['gust'] = 45.0  # Strong gusts
    
    print("\nWeather Conditions:")
    print(f"  Temperature: {poor_weather['temperature_c_aus']}°C")
    print(f"  Wind Speed: {poor_weather['wind_speed_kts_aus']} knots")
    print(f"  Visibility: {poor_weather['visibility_km_aus']} km")
    print(f"  Ceiling: {poor_weather['ceiling_ft_aus']} ft")
    
    risk_score_poor = predict_risk(poor_weather)
    risk_category_poor = interpret_risk_score(risk_score_poor[0])
    
    print(f"\nPredicted Risk Score: {risk_score_poor[0]:.1f}/100")
    print(f"Risk Category: {risk_category_poor}")
    
    print("\n" + "="*60)
    print("To predict for your own data, use:")
    print("  from Src.predict_risk import predict_risk")
    print("  risk_score = predict_risk(your_weather_data)")
    print("="*60)
