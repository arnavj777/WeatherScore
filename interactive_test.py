"""
Interactive Airport Weather Risk Tester
Enter an airport code and weather conditions to get a flight risk score
"""
from Src.predict_zone_risk import predict_zone_risk, interpret_risk_score, ZONES
from Src.load_airports import load_airport_mapping, get_all_airports_by_zone

# Load airports from Excel file
AIRPORT_ZONES = load_airport_mapping()

# Fallback hardcoded airports if Excel file not available
AIRPORT_ZONES_FALLBACK = {
    # Northeast
    'BOS': 'Northeast', 'JFK': 'Northeast', 'LGA': 'Northeast', 'EWR': 'Northeast',
    'PHL': 'Northeast', 'BWI': 'Northeast', 'IAD': 'Northeast', 'DCA': 'Northeast',
    'PWM': 'Northeast', 'BTV': 'Northeast', 'ALB': 'Northeast', 'SYR': 'Northeast',
    
    # Pacific Coast
    'LAX': 'PacificCoast', 'SEA': 'PacificCoast', 'SFO': 'PacificCoast', 'SAN': 'PacificCoast',
    'LAS': 'PacificCoast', 'PDX': 'PacificCoast', 'SNA': 'PacificCoast', 'SJC': 'PacificCoast',
    'SMF': 'PacificCoast', 'BUR': 'PacificCoast', 'OAK': 'PacificCoast', 'BFL': 'PacificCoast',
    'EUG': 'PacificCoast', 'RDM': 'PacificCoast', 'SPD': 'PacificCoast', 'VGT': 'PacificCoast',
    
    # Rocky Mountains
    'DEN': 'RockyMountains', 'SLC': 'RockyMountains', 'ABQ': 'RockyMountains', 'PHX': 'RockyMountains',
    'BOI': 'RockyMountains', 'BZN': 'RockyMountains', 'BIL': 'RockyMountains', 'COS': 'RockyMountains',
    'BUF': 'RockyMountains', 'ASE': 'RockyMountains', 'TUS': 'RockyMountains', 'FAT': 'RockyMountains',
    
    # Central Plains
    'ORD': 'CentralPlains', 'OKC': 'CentralPlains', 'DFW': 'CentralPlains', 'IAH': 'CentralPlains',
    'MSP': 'CentralPlains', 'STL': 'CentralPlains', 'MCI': 'CentralPlains', 'ICT': 'CentralPlains',
    'AUS': 'CentralPlains', 'SAT': 'CentralPlains', 'HOU': 'CentralPlains', 'DAL': 'CentralPlains',
    'LNK': 'CentralPlains', 'OMA': 'CentralPlains', 'DSM': 'CentralPlains', 'FAR': 'CentralPlains',
    
    # Southeast
    'ATL': 'Southeast', 'MIA': 'Southeast', 'CLT': 'Southeast', 'MCO': 'Southeast',
    'TPA': 'Southeast', 'FLL': 'Southeast', 'BNA': 'Southeast', 'RDU': 'Southeast',
    'JAX': 'Southeast', 'RSW': 'Southeast', 'MSY': 'Southeast', 'SAV': 'Southeast',
    'CHS': 'Southeast', 'GSP': 'Southeast', 'CHA': 'Southeast', 'TLH': 'Southeast',
    'GNV': 'Southeast', 'MKY': 'Southeast', 'PNS': 'Southeast', 'MSY': 'Southeast',
}

def get_airport_zone(airport_code):
    """Map airport code to zone"""
    airport_code = airport_code.upper()
    
    # First check the Excel-loaded mapping
    if airport_code in AIRPORT_ZONES:
        return AIRPORT_ZONES[airport_code]
    
    # Then check ZONES dictionary
    for zone, airports in ZONES.items():
        if airport_code in airports:
            return zone
    
    return None

def get_weather_input():
    """Prompt user for weather conditions"""
    print("\n" + "="*70)
    print("ENTER WEATHER CONDITIONS")
    print("="*70)
    print("\nEnter values (press Enter for defaults):\n")
    
    weather = {}
    
    # Basic weather parameters
    temp = input("Temperature (°C) [default: 20]: ").strip()
    weather['temperature_c'] = float(temp) if temp else 20.0
    
    dewpoint = input("Dewpoint (°C) [default: 15]: ").strip()
    weather['dewpoint_c'] = float(dewpoint) if dewpoint else 15.0
    
    wind_dir = input("Wind Direction (0-360°) [default: 270]: ").strip()
    weather['wind_direction'] = float(wind_dir) if wind_dir else 270.0
    
    wind_speed = input("Wind Speed (knots) [default: 12]: ").strip()
    weather['wind_speed_kts'] = float(wind_speed) if wind_speed else 12.0
    
    gust = input("Wind Gusts (knots) [default: 15]: ").strip()
    weather['gust'] = float(gust) if gust else 15.0
    
    visibility = input("Visibility (km) [default: 10]: ").strip()
    weather['visibility_km'] = float(visibility) if visibility else 10.0
    
    ceiling = input("Ceiling (feet) [default: 5000]: ").strip()
    weather['ceiling_ft'] = float(ceiling) if ceiling else 5000.0
    
    pressure = input("Sea Level Pressure (mb) [default: 1013.25]: ").strip()
    weather['sea_level_pressure_mb'] = float(pressure) if pressure else 1013.25
    
    humidity = input("Relative Humidity (%) [default: 65]: ").strip()
    weather['relh'] = float(humidity) if humidity else 65.0
    
    print("\n--- Advanced Parameters (press Enter for calculated values) ---\n")
    
    # Calculated/engineered features
    temp_spread = input("Temperature Spread (temp - dewpoint) [auto]: ").strip()
    weather['temp_spread'] = float(temp_spread) if temp_spread else (weather['temperature_c'] - weather['dewpoint_c'])
    
    gust_factor = input("Gust Factor (gust/speed) [auto]: ").strip()
    weather['gust_factor'] = float(gust_factor) if gust_factor else (weather['gust'] / weather['wind_speed_kts'] if weather['wind_speed_kts'] > 0 else 1.0)
    
    ceiling_vis = input("Ceiling/Visibility Ratio [auto]: ").strip()
    weather['ceiling_vis_ratio'] = float(ceiling_vis) if ceiling_vis else (weather['ceiling_ft'] / weather['visibility_km'] / 3280.84)
    
    pressure_change = input("Pressure Change (mb) [default: 0]: ").strip()
    weather['pressure_change'] = float(pressure_change) if pressure_change else 0.0
    
    weather['humidity'] = weather['relh']  # Same as relh
    
    hour = input("Hour (0-23) [default: 14]: ").strip()
    weather['hour'] = int(hour) if hour else 14
    
    month = input("Month (1-12) [default: 6]: ").strip()
    weather['month'] = int(month) if month else 6
    
    is_night = input("Is Night? (0=day, 1=night) [default: 0]: ").strip()
    weather['is_night'] = int(is_night) if is_night else 0
    
    departure_hour = input("Departure Hour (0-23) [default: 14]: ").strip()
    weather['departure_hour'] = int(departure_hour) if departure_hour else 14
    
    return weather

def main():
    print("="*70)
    print("AIRPORT WEATHER RISK PREDICTOR")
    print("="*70)
    
    # Load airports from Excel
    airports_by_zone = get_all_airports_by_zone()
    
    print("\nSupports international airports from Excel file!")
    print(f"\nTotal airports loaded: {len(AIRPORT_ZONES)}")
    
    # Display airports by zone
    if airports_by_zone:
        for zone, airports in sorted(airports_by_zone.items()):
            codes = [a['code'] for a in airports[:8]]  # Show first 8
            print(f"\n  {zone}: {', '.join(codes)}" + ("..." if len(airports) > 8 else ""))
    
    # Get airport code
    print("\n" + "="*70)
    airport_code = input("Enter Airport Code (e.g., AUS, BOS, JFK, LAX): ").strip().upper()
    
    zone = get_airport_zone(airport_code)
    
    if not zone:
        print(f"\n❌ Error: Airport '{airport_code}' not recognized")
        print("Please enter a 3-letter US airport code (e.g., AUS, BOS, JFK, LAX, DEN)")
        return
    
    print(f"\n✓ {airport_code} is in the {zone} zone")
    
    # Get weather conditions
    weather = get_weather_input()
    
    # Display weather summary
    print("\n" + "="*70)
    print("WEATHER CONDITIONS SUMMARY")
    print("="*70)
    print(f"\nTemperature: {weather['temperature_c']}°C")
    print(f"Dewpoint: {weather['dewpoint_c']}°C")
    print(f"Wind: {weather['wind_direction']}° at {weather['wind_speed_kts']} kts")
    print(f"Gusts: {weather['gust']} kts")
    print(f"Visibility: {weather['visibility_km']} km")
    print(f"Ceiling: {weather['ceiling_ft']} ft")
    print(f"Humidity: {weather['humidity']}%")
    
    # Make prediction
    print("\n" + "="*70)
    print("CALCULATING RISK...")
    print("="*70)
    
    try:
        risk_score = predict_zone_risk(zone, weather)
        category = interpret_risk_score(risk_score[0])
        
        # Risk level emoji
        score = risk_score[0]
        if score < 20:
            emoji = "🟢"
        elif score < 60:
            emoji = "🟡"
        elif score < 80:
            emoji = "🟠"
        else:
            emoji = "🔴"
        
        print(f"\n{emoji} FLIGHT RISK SCORE: {score:.1f}/100")
        print(f"\nCategory: {category}")
        
        # Interpretation
        print("\n" + "="*70)
        print("INTERPRETATION")
        print("="*70)
        
        if score < 20:
            print("\n✓ Excellent weather conditions")
            print("✓ Low flight risk - normal operations expected")
        elif score < 40:
            print("\n✓ Good weather conditions")
            print("✓ Minor concerns - operations should proceed normally")
        elif score < 60:
            print("\n⚠ Moderate weather concerns")
            print("⚠ Some delays possible - monitor conditions")
        elif score < 80:
            print("\n⚠ Significant weather issues")
            print("⚠ Delays likely - consider contingency plans")
        else:
            print("\n⚠⚠ DANGEROUS WEATHER CONDITIONS ⚠⚠")
            print("⚠ Delays/cancellations likely - exercise caution")
        
    except Exception as e:
        print(f"\n❌ Error calculating risk: {e}")
        print("Please check your input values")

if __name__ == "__main__":
    main()
