"""
Custom Weather Testing Script
Modify the weather conditions below and run this script to test
"""
from Src.predict_zone_risk import predict_zone_risk, interpret_risk_score, ZONES

# MODIFY THESE WEATHER CONDITIONS TO TEST YOUR OWN SCENARIOS
custom_weather = {
    'temperature_c': 20.0,
    'dewpoint_c': 15.0,
    'wind_direction': 270,
    'wind_speed_kts': 12.0,
    'gust': 15.0,
    'visibility_km': 10.0,
    'ceiling_ft': 5000.0,
    'sea_level_pressure_mb': 1013.25,
    'relh': 65.0,
    'temp_spread': 5.0,
    'gust_factor': 1.25,
    'ceiling_vis_ratio': 2.0,
    'pressure_change': 0.0,
    'humidity': 65.0,
    'hour': 14,
    'month': 6,
    'is_night': 0,
    'departure_hour': 14
}

def test_custom_weather():
    """Test custom weather conditions across all zones"""
    
    print("="*70)
    print("CUSTOM WEATHER TESTING")
    print("="*70)
    
    print("\nYour Weather Conditions:")
    print(f"  Temperature: {custom_weather['temperature_c']}°C")
    print(f"  Visibility: {custom_weather['visibility_km']} km")
    print(f"  Ceiling: {custom_weather['ceiling_ft']} ft")
    print(f"  Wind Speed: {custom_weather['wind_speed_kts']} kts")
    print(f"  Wind Gusts: {custom_weather['gust']} kts")
    print(f"  Humidity: {custom_weather['humidity']}%")
    
    print("\n" + "="*70)
    print("RISK PREDICTIONS FOR ALL ZONES")
    print("="*70)
    
    results = {}
    for zone_name in ZONES.keys():
        try:
            risk_score = predict_zone_risk(zone_name, custom_weather)
            category = interpret_risk_score(risk_score[0])
            results[zone_name] = risk_score[0]
            
            # Risk level emoji
            emoji = "🟢" if risk_score[0] < 20 else "🟡" if risk_score[0] < 60 else "🟠" if risk_score[0] < 80 else "🔴"
            
            print(f"\n{zone_name} {emoji}")
            print(f"  Risk Score: {risk_score[0]:.1f}/100")
            print(f"  Category: {category}")
        except Exception as e:
            print(f"\n{zone_name} ❌")
            print(f"  Error: {e}")
            results[zone_name] = None
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY - RISK COMPARISON")
    print("="*70)
    
    valid_results = {k: v for k, v in results.items() if v is not None}
    if valid_results:
        sorted_results = sorted(valid_results.items(), key=lambda x: x[1])
        
        print("\nLowest Risk:")
        print(f"  {sorted_results[0][0]}: {sorted_results[0][1]:.1f}/100")
        
        print("\nHighest Risk:")
        print(f"  {sorted_results[-1][0]}: {sorted_results[-1][1]:.1f}/100")

if __name__ == "__main__":
    test_custom_weather()
