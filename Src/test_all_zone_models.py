"""
Test all zone models with sample weather data
"""
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Src.predict_zone_risk import predict_zone_risk, ZONES, interpret_risk_score
import numpy as np
import warnings
warnings.filterwarnings('ignore')

def test_all_zones():
    """Test all zone models with sample weather conditions"""
    
    # Sample weather data - good conditions
    sample_weather = {
        'temperature_c': 15.0,
        'dewpoint_c': 10.0,
        'wind_direction': 270,
        'wind_speed_kts': 10.0,
        'gust': 12.0,
        'visibility_km': 10.0,
        'ceiling_ft': 5000.0,
        'sea_level_pressure_mb': 1013.25,
        'relh': 65.0,
        'temp_spread': 5.0,
        'gust_factor': 1.2,
        'ceiling_vis_ratio': 2.0,
        'pressure_change': 0.0,
        'humidity': 65.0,
        'hour': 12,
        'month': 6,
        'is_night': 0,
        'departure_hour': 12
    }
    
    print("="*70)
    print("TESTING ALL ZONE MODELS")
    print("="*70)
    print("\nWeather Conditions:")
    print(f"  Temperature: {sample_weather['temperature_c']}°C")
    print(f"  Visibility: {sample_weather['visibility_km']} km")
    print(f"  Ceiling: {sample_weather['ceiling_ft']} ft")
    print(f"  Wind Speed: {sample_weather['wind_speed_kts']} kts")
    print()
    
    results = {}
    
    for zone_name in ZONES.keys():
        try:
            risk_score = predict_zone_risk(zone_name, sample_weather)
            category = interpret_risk_score(risk_score[0] if isinstance(risk_score, np.ndarray) else risk_score)
            results[zone_name] = {
                'score': risk_score[0] if isinstance(risk_score, np.ndarray) else risk_score,
                'category': category
            }
        except Exception as e:
            results[zone_name] = {
                'error': str(e)
            }
    
    # Print results
    print("="*70)
    print("RESULTS FOR ALL ZONES")
    print("="*70)
    print()
    
    for zone_name in ZONES.keys():
        print(f"{zone_name}:")
        if 'error' in results[zone_name]:
            print(f"  ❌ Error: {results[zone_name]['error']}")
        else:
            print(f"  Risk Score: {results[zone_name]['score']:.1f}/100")
            print(f"  Category: {results[zone_name]['category']}")
        print()
    
    # Summary
    print("="*70)
    print("SUMMARY")
    print("="*70)
    print()
    
    successful_zones = []
    for zone_name, result in results.items():
        if 'error' not in result:
            successful_zones.append(zone_name)
            print(f"✅ {zone_name} - Score: {result['score']:.1f}")
        else:
            print(f"❌ {zone_name} - Failed")
    
    print(f"\nSuccessfully tested {len(successful_zones)}/{len(ZONES)} zones")

if __name__ == "__main__":
    test_all_zones()
