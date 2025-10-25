"""
Example script to test the model with your own custom weather data
"""
from predict_risk import predict_risk, interpret_risk_score

# Example 1: Clear weather conditions
clear_weather = {
    'temperature_c_aus': 20.0,
    'dewpoint_c_aus': 12.0,
    'wind_direction_aus': 270,
    'wind_speed_kts_aus': 8.0,
    'visibility_km_aus': 15.0,
    'ceiling_ft_aus': 6000.0,
    'sea_level_pressure_mb_aus': 1013.5,
    'gust': 0.0,
    'relh': 60.0,
    'temp_spread': 8.0,
    'gust_factor': 0.0,
    'ceiling_vis_ratio': 1.2,
    'pressure_change': 0.0,
    'humidity': 60.0,
    'hour': 14,
    'month': 7,
    'is_night': 0
}

# Example 2: Poor weather conditions
poor_weather = {
    'temperature_c_aus': 5.0,
    'dewpoint_c_aus': 4.0,
    'wind_direction_aus': 300,
    'wind_speed_kts_aus': 25.0,
    'visibility_km_aus': 1.0,
    'ceiling_ft_aus': 400.0,
    'sea_level_pressure_mb_aus': 1005.0,
    'gust': 35.0,
    'relh': 95.0,
    'temp_spread': 1.0,
    'gust_factor': 1.4,
    'ceiling_vis_ratio': 120.0,
    'pressure_change': -2.0,
    'humidity': 95.0,
    'hour': 6,
    'month': 12,
    'is_night': 1
}

# Example 3: Marginal conditions
marginal_weather = {
    'temperature_c_aus': 12.0,
    'dewpoint_c_aus': 8.0,
    'wind_direction_aus': 180,
    'wind_speed_kts_aus': 15.0,
    'visibility_km_aus': 5.0,
    'ceiling_ft_aus': 1500.0,
    'sea_level_pressure_mb_aus': 1010.0,
    'gust': 22.0,
    'relh': 75.0,
    'temp_spread': 4.0,
    'gust_factor': 1.47,
    'ceiling_vis_ratio': 0.94,
    'pressure_change': -1.0,
    'humidity': 75.0,
    'hour': 10,
    'month': 3,
    'is_night': 0
}

Test_weather = {
    'temperature_c_aus': 29.0,
    'dewpoint_c_aus': 25.0,
    'wind_direction_aus': 180,
    'wind_speed_kts_aus': 20.0,
    'visibility_km_aus': 8.0,
    'ceiling_ft_aus': 2500.0,
    'sea_level_pressure_mb_aus': 1010.0,
    'gust': 28.0,
    'relh': 80.0,
    'temp_spread': 4.0,
    'gust_factor': 1.4,
    'ceiling_vis_ratio': 1.0,
    'pressure_change': -0.5,
    'humidity': 80.0,
    'hour': 14,
    'month': 7,
    'is_night': 0
}


def test_weather(weather, label):
    """Test weather conditions and print results"""
    print("=" * 70)
    print(f"TESTING: {label}")
    print("=" * 70)
    
    print(f"\nWeather Conditions:")
    print(f"  Temperature: {weather['temperature_c_aus']:.1f}°C")
    print(f"  Wind: {weather['wind_speed_kts_aus']:.1f} kts from {weather['wind_direction_aus']:.0f}°")
    print(f"  Visibility: {weather['visibility_km_aus']:.1f} km")
    print(f"  Ceiling: {weather['ceiling_ft_aus']:.0f} ft")
    print(f"  Gusts: {weather['gust']:.1f} kts")
    
    # Get prediction
    risk_score = predict_risk(weather)
    risk_category = interpret_risk_score(risk_score[0])
    
    print(f"\n{'='*70}")
    print(f"RESULT: {risk_category}")
    print(f"Risk Score: {risk_score[0]:.1f}/100")
    print(f"{'='*70}\n")
    
    return risk_score[0]

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("CUSTOM WEATHER DATA TESTING")
    print("=" * 70)
    print("\nThis script demonstrates how to test the model with your own data.")
    print("You can modify the weather dictionaries above to test different scenarios.\n")
    
    # Test different weather conditions
    clear_score = test_weather(clear_weather, "CLEAR WEATHER")
    poor_score = test_weather(poor_weather, "POOR WEATHER")  
    marginal_score = test_weather(marginal_weather, "MARGINAL WEATHER")
    test_score = test_weather(Test_weather, "TEST WEATHER")
    
    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    # print(f"\nClear Weather Risk:     {clear_score:.1f}/100")
    # print(f"Marginal Weather Risk: {marginal_score:.1f}/100")
    # print(f"Poor Weather Risk:     {poor_score:.1f}/100")
    print(f"Test Weather Risk:     {test_score:.1f}/100")
    print("\n" + "=" * 70)
    #print("\nTo test your own data, modify the weather dictionaries in this file")
    print("and run: python Src/example_test.py")
    print("=" * 70 + "\n")
