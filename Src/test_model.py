import pandas as pd
import numpy as np
from predict_risk import predict_risk, interpret_risk_score

def get_weather_input():
    """Get weather input from user"""
    print("\n" + "="*60)
    print("FLIGHT RISK PREDICTION - INPUT YOUR WEATHER DATA")
    print("="*60)
    print("\nPlease enter the weather conditions:")
    print("(Press Enter to use default values or type 'skip' to skip optional fields)\n")
    
    # Required weather parameters
    weather = {}
    
    try:
        # Temperature
        temp_input = input("Temperature (°C) [15.0]: ").strip()
        weather['temperature_c_aus'] = float(temp_input) if temp_input else 15.0
        
        # Dewpoint
        dewpoint_input = input("Dewpoint (°C) [10.0]: ").strip()
        weather['dewpoint_c_aus'] = float(dewpoint_input) if dewpoint_input else 10.0
        
        # Wind direction
        wind_dir_input = input("Wind Direction (degrees 0-360) [270]: ").strip()
        weather['wind_direction_aus'] = float(wind_dir_input) if wind_dir_input else 270.0
        
        # Wind speed
        wind_speed_input = input("Wind Speed (knots) [5.0]: ").strip()
        weather['wind_speed_kts_aus'] = float(wind_speed_input) if wind_speed_input else 5.0
        
        # Visibility
        vis_input = input("Visibility (km) [10.0]: ").strip()
        weather['visibility_km_aus'] = float(vis_input) if vis_input else 10.0
        
        # Ceiling
        ceiling_input = input("Ceiling (feet) [5000.0]: ").strip()
        weather['ceiling_ft_aus'] = float(ceiling_input) if ceiling_input else 5000.0
        
        # Pressure
        pressure_input = input("Sea Level Pressure (mb) [1013.0]: ").strip()
        weather['sea_level_pressure_mb_aus'] = float(pressure_input) if pressure_input else 1013.0
        
        # Gust
        gust_input = input("Wind Gusts (knots) [0.0]: ").strip()
        weather['gust'] = float(gust_input) if gust_input else 0.0
        
        # Relative humidity
        hum_input = input("Relative Humidity (%) [70.0]: ").strip()
        weather['relh'] = float(hum_input) if hum_input else 70.0
        
        # Engineered features (can be calculated automatically or input)
        print("\n" + "-"*60)
        print("OPTIONAL: Engineered Features")
        print("(These can be calculated automatically or entered manually)")
        print("-"*60)
        
        calc_engineered = input("\nCalculate engineered features automatically? (y/n) [y]: ").strip().lower()
        
        if calc_engineered == 'n' or calc_engineered == 'no':
            temp_spread_input = input(f"Temperature Spread (temp - dewpoint) [{weather['temperature_c_aus'] - weather['dewpoint_c_aus']:.1f}]: ").strip()
            weather['temp_spread'] = float(temp_spread_input) if temp_spread_input else weather['temperature_c_aus'] - weather['dewpoint_c_aus']
            
            gust_factor_input = input(f"Gust Factor [{weather['gust'] / (weather['wind_speed_kts_aus'] + 1):.2f}]: ").strip()
            weather['gust_factor'] = float(gust_factor_input) if gust_factor_input else weather['gust'] / (weather['wind_speed_kts_aus'] + 1)
            
            ceiling_vis_input = input(f"Ceiling/Visibility Ratio [{(weather['ceiling_ft_aus'] / (weather['visibility_km_aus'] * 1000 / 3.28084 + 1)):.2f}]: ").strip()
            weather['ceiling_vis_ratio'] = float(ceiling_vis_input) if ceiling_vis_input else weather['ceiling_ft_aus'] / (weather['visibility_km_aus'] * 1000 / 3.28084 + 1)
            
            weather['pressure_change'] = 0.0
        else:
            # Calculate automatically
            weather['temp_spread'] = weather['temperature_c_aus'] - weather['dewpoint_c_aus']
            weather['gust_factor'] = weather['gust'] / (weather['wind_speed_kts_aus'] + 1)
            weather['ceiling_vis_ratio'] = weather['ceiling_ft_aus'] / (weather['visibility_km_aus'] * 1000 / 3.28084 + 1)
            weather['pressure_change'] = 0.0
        
        # Humidity (same as relh)
        weather['humidity'] = weather['relh']
        
        # Time features
        hour_input = input("\nHour (0-23) [12]: ").strip()
        weather['hour'] = int(hour_input) if hour_input else 12
        
        month_input = input("Month (1-12) [6]: ").strip()
        weather['month'] = int(month_input) if month_input else 6
        
        night_input = input("Is it night? (0=no, 1=yes) [0]: ").strip()
        weather['is_night'] = int(night_input) if night_input else 0
        
    except ValueError as e:
        print(f"\nError: Invalid input. Please enter numeric values.")
        return None
    except KeyboardInterrupt:
        print("\n\nCancelled by user.")
        return None
    
    return weather

def display_input_summary(weather):
    """Display summary of input weather conditions"""
    print("\n" + "="*60)
    print("WEATHER CONDITIONS SUMMARY")
    print("="*60)
    print(f"\nTemperature:      {weather['temperature_c_aus']:.1f}°C")
    print(f"Dewpoint:         {weather['dewpoint_c_aus']:.1f}°C")
    print(f"Wind:             {weather['wind_speed_kts_aus']:.1f} kts from {weather['wind_direction_aus']:.0f}°")
    print(f"Visibility:       {weather['visibility_km_aus']:.1f} km")
    print(f"Ceiling:          {weather['ceiling_ft_aus']:.0f} ft")
    print(f"Pressure:         {weather['sea_level_pressure_mb_aus']:.1f} mb")
    print(f"Gusts:            {weather['gust']:.1f} kts")
    print(f"Humidity:         {weather['relh']:.0f}%")
    print(f"\nTime:             Hour {weather['hour']}, Month {weather['month']}, Night: {'Yes' if weather['is_night'] else 'No'}")

def main():
    print("="*60)
    print("FLIGHT RISK SCORING MODEL - INTERACTIVE TESTER")
    print("="*60)
    print("\nThis tool allows you to test your own weather data")
    print("and get a flight risk prediction (0-100 scale).")
    print("\n100 = Maximum Flight Risk")
    print("0 = Minimal Flight Risk")
    
    while True:
        # Get user input
        weather = get_weather_input()
        
        if weather is None:
            break
        
        # Display input summary
        display_input_summary(weather)
        
        # Confirm before predicting
        print("\n" + "-"*60)
        confirm = input("Predict risk with these conditions? (y/n): ").strip().lower()
        
        if confirm in ['y', 'yes']:
            try:
                # Make prediction
                risk_score = predict_risk(weather)
                risk_category = interpret_risk_score(risk_score[0])
                
                # Display results
                print("\n" + "="*60)
                print("PREDICTION RESULTS")
                print("="*60)
                print(f"\n⚠️  RISK SCORE: {risk_score[0]:.1f}/100")
                print(f"📊 CATEGORY: {risk_category}")
                print("\n" + "="*60)
                
                # Risk interpretation
                print("\nRisk Breakdown:")
                if risk_score[0] < 20:
                    print("✅ Conditions are SAFE for flight operations")
                elif risk_score[0] < 40:
                    print("✅ Conditions are generally safe with minor caution")
                elif risk_score[0] < 60:
                    print("⚠️  Proceed with CAUTION - marginal conditions")
                elif risk_score[0] < 80:
                    print("⚠️⚠️  HIGH RISK - Significant hazards present")
                else:
                    print("🚨🚨 VERY HIGH RISK - RECOMMEND GROUNDING")
                
            except Exception as e:
                print(f"\n❌ Error making prediction: {e}")
                print("Please check your input values and try again.")
        
        # Ask if user wants to test another scenario
        print("\n" + "-"*60)
        continue_input = input("\nTest another scenario? (y/n): ").strip().lower()
        if continue_input not in ['y', 'yes']:
            break
    
    print("\n" + "="*60)
    print("Thank you for using the Flight Risk Scoring Model!")
    print("="*60)

if __name__ == "__main__":
    main()
