import pandas as pd
import numpy as np
import os
from glob import glob

# Define zones and their airports
ZONES = {
    'Northeast': ['BOS', 'JFK'],
    'PacificCoast': ['LAX', 'SEA'],
    'RockyMountains': ['DEN'],  # Only one airport
    'CentralPlains': ['ORD', 'OKC'],
    'Southeast': ['ATL', 'MIA']
}

def parse_airport_weather(filepath):
    """Load and parse a single airport weather CSV file"""
    print(f"  Loading {os.path.basename(filepath)}...")
    
    try:
        df = pd.read_csv(filepath, low_memory=False)
        
        # Check what columns we have
        print(f"    Columns: {list(df.columns[:10])}")
        print(f"    Shape: {df.shape}")
        
        # Try to detect the format
        if 'station' in df.columns and 'valid' in df.columns:
            # AUS-style format
            return parse_aus_format(df)
        else:
            # Try METAR format
            return parse_metar_format(df)
    
    except Exception as e:
        print(f"    Error loading {filepath}: {e}")
        return None

def parse_aus_format(df):
    """Parse AUS-style airport data format"""
    # Convert timestamp
    df['valid'] = pd.to_datetime(df['valid'])
    df['date'] = df['valid'].dt.date
    
    # Temperature (F to C)
    df['temperature_c'] = (df['tmpf'] - 32) * 5/9
    
    # Dewpoint (F to C)
    df['dewpoint_c'] = (df['dwpf'] - 32) * 5/9
    
    # Wind
    df['wind_direction'] = df['drct']
    df['wind_speed_kts'] = df['sknt']
    
    # Visibility (miles to km)
    df['visibility_km'] = df['vsby'] * 1.60934
    
    # Ceiling from sky layers
    df['ceiling_ft'] = df[['skyl1', 'skyl2', 'skyl3']].apply(
        lambda row: min([x for x in row if pd.notna(x)], default=np.nan), axis=1
    )
    
    # Pressure
    df['sea_level_pressure_mb'] = df['mslp']
    
    # Other features
    df['gust'] = df['gust']
    df['relh'] = df['relh']
    
    return df

def parse_metar_format(df):
    """Parse METAR format data (like 4152601.csv)"""
    # This would use the METAR parsing logic from data_processing.py
    # For now, return as-is and handle in main processing
    print("    METAR format detected - using basic parsing")
    return df

def process_zone(zone_name, airports):
    """Process all airports in a zone and combine them"""
    print(f"\n{'='*60}")
    print(f"Processing Zone: {zone_name}")
    print(f"{'='*60}")
    
    zone_data = []
    
    for airport in airports:
        filepath = f"Data/{zone_name}/{airport}.csv"
        
        if not os.path.exists(filepath):
            print(f"  Warning: {filepath} not found, skipping")
            continue
        
        df = parse_airport_weather(filepath)
        
        if df is not None:
            # Add zone and airport identifiers
            df['zone'] = zone_name
            df['airport'] = airport
            zone_data.append(df)
    
    if not zone_data:
        print(f"  No data found for zone {zone_name}")
        return None
    
    # Combine all airports in the zone
    combined = pd.concat(zone_data, ignore_index=True)
    
    print(f"\n  Combined data shape: {combined.shape}")
    print(f"  Date range: {combined['date'].min()} to {combined['date'].max()}")
    print(f"  Airports: {combined['airport'].unique()}")
    
    return combined

def engineer_features(df):
    """Engineer additional features for the model"""
    # Temperature spread
    df['temp_spread'] = df['temperature_c'] - df['dewpoint_c']
    
    # Wind gust factor
    df['gust_factor'] = df['gust'] / (df['wind_speed_kts'] + 1)
    
    # Ceiling to visibility ratio
    df['ceiling_vis_ratio'] = df['ceiling_ft'] / (df['visibility_km'] * 1000 / 3.28084 + 1)
    
    # Pressure change (will be calculated per zone)
    df['pressure_change'] = df['sea_level_pressure_mb'].diff().fillna(0)
    
    # Humidity
    df['humidity'] = df['relh'].fillna(50)
    
    # Time features
    if 'valid' in df.columns:
        df['hour'] = pd.to_datetime(df['valid']).dt.hour
        df['month'] = pd.to_datetime(df['valid']).dt.month
        df['is_night'] = ((df['hour'] >= 20) | (df['hour'] <= 6)).astype(int)
    
    return df

def main():
    print("="*60)
    print("MULTI-ZONE WEATHER DATA PROCESSING")
    print("="*60)
    
    all_zones_data = {}
    
    # Process each zone
    for zone_name, airports in ZONES.items():
        zone_df = process_zone(zone_name, airports)
        
        if zone_df is not None:
            # Engineer features
            zone_df = engineer_features(zone_df)
            all_zones_data[zone_name] = zone_df
    
    # Save processed data for each zone
    os.makedirs('Data/processed_zones', exist_ok=True)
    
    for zone_name, df in all_zones_data.items():
        output_path = f"Data/processed_zones/{zone_name}_weather.csv"
        df.to_csv(output_path, index=False)
        print(f"\n✅ Saved {zone_name} data to {output_path}")
    
    # Summary
    print("\n" + "="*60)
    print("PROCESSING SUMMARY")
    print("="*60)
    
    for zone_name, df in all_zones_data.items():
        print(f"\n{zone_name}:")
        print(f"  Records: {len(df):,}")
        print(f"  Features: {df.shape[1]}")
        print(f"  Airports: {', '.join(df['airport'].unique())}")
        print(f"  Date range: {df['date'].min()} to {df['date'].max()}")
    
    print("\n✅ Zone data processing complete!")
    print("\nNext step: Load flight delay data and train models")

if __name__ == "__main__":
    main()
