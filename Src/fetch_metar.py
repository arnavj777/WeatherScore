"""
Fetch real-time METAR weather data from NOAA API
"""
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import re

def fetch_metar_data(station_code):
    """
    Fetch current METAR data from NOAA for a given airport code
    
    Args:
        station_code: 4-letter ICAO station code (e.g., 'KAUS' for Austin)
    
    Returns:
        dict: Parsed METAR data or None if error
    """
    try:
        # NOAA API endpoint for METAR data
        url = f"https://aviationweather.gov/api/data/metar?ids={station_code}&format=xml"
        
        print(f"Fetching METAR data for {station_code}...")
        response = requests.get(url, timeout=10)
        
        if response.status_code != 200:
            print(f"Error: API returned status code {response.status_code}")
            return None
        
        # Parse XML response
        root = ET.fromstring(response.content)
        
        # Find the rawtext METAR data (try both possible tags)
        rawtext = root.find('.//rawText') or root.find('.//raw_text')
        if rawtext is None:
            print("Error: No METAR data found in response")
            # Debug: print the XML structure
            print("XML content preview:")
            print(ET.tostring(root, encoding='unicode')[:500])
            return None
        
        metar_text = rawtext.text
        print(f"METAR: {metar_text}")
        
        # Parse METAR text
        parsed_data = parse_metar_text(metar_text)
        
        return parsed_data
        
    except requests.exceptions.RequestException as e:
        print(f"Network error fetching METAR data: {e}")
        return None
    except ET.ParseError as e:
        print(f"Error parsing XML response: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def parse_metar_text(metar_text):
    """
    Parse METAR text into structured data
    
    Args:
        metar_text: Raw METAR string
    
    Returns:
        dict: Parsed weather data
    """
    data = {}
    
    try:
        # Parse temperature (e.g., "TEMP/DEWPOINT" or "06/M01")
        temp_match = re.search(r'\b(\d{2})/(\d{2}|M\d{2})\b', metar_text)
        if temp_match:
            temp_str = temp_match.group(1)
            dew_str = temp_match.group(2)
            
            data['temperature_c'] = float(temp_str) if temp_str[0] != 'M' else -float(temp_str[1:])
            data['dewpoint_c'] = float(dew_str) if dew_str[0] != 'M' else -float(dew_str[1:])
        
        # Parse wind (e.g., "18015G22KT")
        wind_match = re.search(r'(\d{3})(\d{2,3})(G(\d{2,3}))?KT', metar_text)
        if wind_match:
            data['wind_direction'] = float(wind_match.group(1))
            data['wind_speed_kts'] = float(wind_match.group(2))
            if wind_match.group(4):
                data['gust'] = float(wind_match.group(4))
            else:
                data['gust'] = data['wind_speed_kts']
        
        # Parse visibility (e.g., "10SM" or "1 1/2SM" or "9999" for meters)
        vis_match = re.search(r'(\d+)\s*(\d/\d)?SM', metar_text)
        if vis_match:
            vis_miles = float(vis_match.group(1))
            if vis_match.group(2):  # Handle fractions like "1 1/2SM"
                fraction = eval(vis_match.group(2))
                vis_miles += fraction
            data['visibility_km'] = vis_miles * 1.60934
        else:
            vis_match = re.search(r'(\d{4})\b', metar_text)
            if vis_match:
                data['visibility_km'] = float(vis_match.group(1)) / 1000.0
        
        # Parse cloud ceiling
        cloud_match = re.search(r'OVC(\d{3})|BKN(\d{3})|SCT(\d{3})', metar_text)
        if cloud_match:
            ceiling_str = cloud_match.group(1) or cloud_match.group(2) or cloud_match.group(3)
            data['ceiling_ft'] = float(ceiling_str) * 100
        elif 'CLR' in metar_text or 'SKC' in metar_text:
            data['ceiling_ft'] = 9999  # Clear skies
        
        # Parse pressure (e.g., "A3012" or "Q1023")
        pressure_match = re.search(r'A(\d{4})|Q(\d{4})', metar_text)
        if pressure_match:
            if pressure_match.group(1):  # Inches of mercury
                inches_hg = float(pressure_match.group(1)) / 100.0
                data['sea_level_pressure_mb'] = inches_hg * 33.8639
            elif pressure_match.group(2):  # Millibars
                data['sea_level_pressure_mb'] = float(pressure_match.group(2)) / 10.0
        
        # Parse relative humidity (calculate from temp/dewpoint)
        if 'temperature_c' in data and 'dewpoint_c' in data:
            temp_c = data['temperature_c']
            dew_c = data['dewpoint_c']
            # Magnus formula for humidity
            es = 6.112 * 10**((7.5*temp_c)/(237.7+temp_c))
            e = 6.112 * 10**((7.5*dew_c)/(237.7+dew_c))
            data['relh'] = (e/es) * 100
            data['humidity'] = data['relh']
        
        # Calculate derived features
        if 'temperature_c' in data and 'dewpoint_c' in data:
            data['temp_spread'] = data['temperature_c'] - data['dewpoint_c']
        
        if 'wind_speed_kts' in data:
            data['gust_factor'] = data['gust'] / max(data['wind_speed_kts'], 1)
        
        if 'ceiling_ft' in data and 'visibility_km' in data:
            data['ceiling_vis_ratio'] = data['ceiling_ft'] / (data['visibility_km'] * 3280.84 + 1)
        
        data['pressure_change'] = 0.0  # Not available in METAR
        
        # Time features
        now = datetime.now()
        data['hour'] = now.hour
        data['month'] = now.month
        data['is_night'] = 1 if 20 <= now.hour or now.hour < 6 else 0
        data['departure_hour'] = now.hour  # Same as current hour for real-time predictions
        
    except Exception as e:
        print(f"Error parsing METAR text: {e}")
        return None
    
    return data

def airport_code_to_icao(airport_code):
    """
    Convert 3-letter IATA code to 4-letter ICAO code
    
    Args:
        airport_code: 3-letter IATA code (e.g., 'AUS')
    
    Returns:
        str: 4-letter ICAO code (e.g., 'KAUS')
    """
    # US airports typically prefix 'K' to IATA code
    # Add more mappings as needed
    us_prefix = 'K'
    return f"{us_prefix}{airport_code.upper()}"

if __name__ == "__main__":
    # Test with Austin
    icao_code = airport_code_to_icao('AUS')
    data = fetch_metar_data(icao_code)
    
    if data:
        print("\nParsed METAR Data:")
        for key, value in data.items():
            print(f"  {key}: {value}")
