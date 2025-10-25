import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import xgboost as xgb
import warnings
import re
from datetime import datetime
warnings.filterwarnings('ignore')

def parse_metar_field(value, field_type='float'):
    """Parse METAR format fields (e.g., '+0128,1' -> 12.8)"""
    if pd.isna(value) or value == '':
        return np.nan
    
    try:
        # Handle METAR format: "+0128,1" where 128 means 12.8
        # Some fields have multiple values separated by commas
        if ',' in str(value):
            parts = str(value).split(',')
            # First part is the main value
            main_value = parts[0]
            
            # Remove + or - sign
            if main_value.startswith('+'):
                sign = 1
                main_value = main_value[1:]
            elif main_value.startswith('-'):
                sign = -1
                main_value = main_value[1:]
            else:
                sign = 1
            
            # Parse number (e.g., "0128" -> 12.8)
            if main_value.isdigit() or main_value.replace('.', '').isdigit():
                num_value = float(main_value)
                # METAR temperature/values are in tenths (e.g., 0128 = 12.8)
                result = sign * num_value / 10.0
                
                # Handle special values like 9999.9 (missing)
                if result == 9999.9 or result == 999.9:
                    return np.nan
                return result
        
        return float(value)
    except:
        return np.nan

def parse_wind_field(value):
    """Parse wind field (e.g., '350,1,N,0082,1' -> direction, speed, quality flags)"""
    if pd.isna(value) or value == '':
        return np.nan, np.nan, np.nan
    
    try:
        parts = str(value).split(',')
        if len(parts) >= 4:
            direction = parse_metar_field(parts[0])
            quality_code = parts[1]
            speed = parse_metar_field(parts[2] + ',' + parts[3])
            
            # Handle missing values
            if direction == 999.9 or speed == 999.9:
                return np.nan, np.nan, np.nan
            
            return direction, speed, quality_code
    except:
        pass
    
    return np.nan, np.nan, np.nan

def parse_visibility_field(value):
    """Parse visibility field (e.g., '016000,1,N,1' -> visibility in meters)"""
    if pd.isna(value) or value == '':
        return np.nan
    
    try:
        parts = str(value).split(',')
        if len(parts) >= 2:
            visibility_str = parts[0]
            if visibility_str.isdigit():
                # Visibility is in meters, sometimes in thousands (e.g., 16000 = 16km)
                visibility = float(visibility_str) / 1000.0  # Convert to km
                
                # Handle missing values (999999)
                if visibility >= 999.0:
                    return np.nan
                return visibility
    except:
        pass
    
    return np.nan

def parse_ceiling_field(value):
    """Parse ceiling height field (e.g., '03353,5,M,N' -> ceiling height)"""
    if pd.isna(value) or value == '':
        return np.nan
    
    try:
        parts = str(value).split(',')
        if len(parts) >= 3:
            height_str = parts[0]
            if height_str.isdigit():
                height = float(height_str)
                
                # Handle missing values
                if height >= 99999:
                    return np.nan
                
                # Convert from code to height (in hundreds of feet)
                # e.g., 03353 might represent 3353 feet
                return height
    except:
        pass
    
    return np.nan

def clean_metar_data(metar_df):
    """Clean and extract useful features from METAR data"""
    print("\nCleaning METAR data...")
    print(f"Original shape: {metar_df.shape}")
    
    # Parse key fields
    print("Parsing METAR fields...")
    
    # Parse temperature
    metar_df['temperature_c'] = metar_df['TMP'].apply(lambda x: parse_metar_field(x))
    
    # Parse dewpoint
    metar_df['dewpoint_c'] = metar_df['DEW'].apply(lambda x: parse_metar_field(x))
    
    # Parse wind
    wind_data = metar_df['WND'].apply(parse_wind_field)
    metar_df['wind_direction'] = [x[0] for x in wind_data]
    metar_df['wind_speed_kts'] = [x[1] for x in wind_data]
    
    # Parse visibility
    metar_df['visibility_km'] = metar_df['VIS'].apply(parse_visibility_field)
    
    # Parse ceiling
    metar_df['ceiling_ft'] = metar_df['CIG'].apply(parse_ceiling_field)
    
    # Parse pressure
    metar_df['sea_level_pressure_mb'] = metar_df['SLP'].apply(lambda x: parse_metar_field(x))
    
    # Parse date
    metar_df['date'] = pd.to_datetime(metar_df['DATE'])
    
    # Keep only parsed columns and key identifiers
    key_columns = ['STATION', 'DATE', 'date', 'temperature_c', 'dewpoint_c', 
                   'wind_direction', 'wind_speed_kts', 'visibility_km', 
                   'ceiling_ft', 'sea_level_pressure_mb']
    
    metar_clean = metar_df[key_columns].copy()
    
    print(f"Cleaned shape: {metar_clean.shape}")
    print(f"Sample of cleaned data:\n{metar_clean.head()}")
    
    return metar_clean

def clean_aus_data(aus_df):
    """Clean and process AUS airport data"""
    print("\nCleaning AUS data...")
    print(f"Original shape: {aus_df.shape}")
    
    # Convert columns to appropriate types
    aus_df['valid'] = pd.to_datetime(aus_df['valid'])
    aus_df['date'] = aus_df['valid'].dt.date
    
    # Convert temperature from Fahrenheit to Celsius
    aus_df['temperature_c'] = (aus_df['tmpf'] - 32) * 5/9
    
    # Convert dewpoint from Fahrenheit to Celsius
    aus_df['dewpoint_c'] = (aus_df['dwpf'] - 32) * 5/9
    
    # Wind data (already in appropriate units)
    aus_df['wind_direction'] = aus_df['drct']
    aus_df['wind_speed_kts'] = aus_df['sknt']
    
    # Visibility (convert from miles to km)
    aus_df['visibility_km'] = aus_df['vsby'] * 1.60934
    
    # Ceiling - need to extract from sky layers
    aus_df['ceiling_ft'] = aus_df[['skyl1', 'skyl2', 'skyl3']].apply(
        lambda row: min([x for x in row if pd.notna(x)], default=np.nan), axis=1
    )
    
    # Pressure
    aus_df['sea_level_pressure_mb'] = aus_df['mslp']
    
    # Key columns
    key_columns = ['station', 'date', 'valid', 'temperature_c', 'dewpoint_c',
                   'wind_direction', 'wind_speed_kts', 'visibility_km',
                   'ceiling_ft', 'sea_level_pressure_mb', 'gust', 'relh']
    
    aus_clean = aus_df[key_columns].copy()
    
    print(f"Cleaned shape: {aus_clean.shape}")
    print(f"Sample of cleaned data:\n{aus_clean.head()}")
    
    return aus_clean

def combine_datasets(metar_clean, aus_clean):
    """Combine both datasets on date"""
    print("\nCombining datasets...")
    
    # Ensure date columns are the same type
    metar_clean['date'] = pd.to_datetime(metar_clean['date']).dt.date
    aus_clean['date'] = pd.to_datetime(aus_clean['date']).dt.date
    
    # Merge on date
    combined = pd.merge(aus_clean, metar_clean, on='date', how='inner', suffixes=('_aus', '_metar'))
    
    print(f"Combined shape: {combined.shape}")
    print(f"Sample of combined data:\n{combined.head()}")
    
    return combined

if __name__ == "__main__":
    # Load data
    print("="*60)
    print("WEATHER DATA PROCESSING FOR FLIGHT RISK SCORING")
    print("="*60)
    
    metar_df = pd.read_csv('Data/4152601.csv', low_memory=False)
    aus_df = pd.read_csv('Data/AUS.csv', low_memory=False)
    
    print(f"\nLoaded METAR data: {metar_df.shape}")
    print(f"Loaded AUS data: {aus_df.shape}")
    
    # Clean data
    metar_clean = clean_metar_data(metar_df)
    aus_clean = clean_aus_data(aus_df)
    
    # Combine datasets
    combined = combine_datasets(metar_clean, aus_clean)
    
    # Save cleaned data
    combined.to_csv('Data/cleaned_weather_data.csv', index=False)
    print("\nCleaned data saved to 'Data/cleaned_weather_data.csv'")
