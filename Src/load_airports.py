"""
Load airport data from Excel file and create airport-to-zone mapping
"""
import pandas as pd
import os

def load_airport_mapping():
    """Load airport data from Excel file"""
    excel_path = 'Data/international_airports_by_region.xlsx'
    
    if not os.path.exists(excel_path):
        print(f"Warning: {excel_path} not found")
        return {}
    
    try:
        df = pd.read_excel(excel_path)
        
        # Create mapping: IATA code -> Zone (capitalize first letter)
        airport_to_zone = {}
        
        for _, row in df.iterrows():
            iata = row['IATA'].upper()
            region = row['Region']
            
            # Convert region to our zone format (capitalize first letter)
            if region.lower() == 'pacificcoast':
                zone = 'PacificCoast'
            elif region.lower() == 'northeast':
                zone = 'Northeast'
            elif region.lower() == 'centralplains':
                zone = 'CentralPlains'
            elif region.lower() == 'rockymountains':
                zone = 'RockyMountains'
            else:
                zone = 'Southeast'  # Default to Southeast
            
            airport_to_zone[iata] = zone
        
        print(f"Loaded {len(airport_to_zone)} airports from Excel file")
        return airport_to_zone
        
    except Exception as e:
        print(f"Error loading airport data: {e}")
        return {}

def get_all_airports_by_zone():
    """Get all airports grouped by zone"""
    excel_path = 'Data/international_airports_by_region.xlsx'
    
    if not os.path.exists(excel_path):
        return {}
    
    try:
        df = pd.read_excel(excel_path)
        
        airports_by_zone = {}
        
        for _, row in df.iterrows():
            iata = row['IATA'].upper()
            airport_name = row['Airport Name']
            region = row['Region']
            
            # Convert region to our zone format
            if region.lower() == 'pacificcoast':
                zone = 'PacificCoast'
            elif region.lower() == 'northeast':
                zone = 'Northeast'
            elif region.lower() == 'centralplains':
                zone = 'CentralPlains'
            elif region.lower() == 'rockymountains':
                zone = 'RockyMountains'
            else:
                zone = 'Southeast'
            
            if zone not in airports_by_zone:
                airports_by_zone[zone] = []
            
            airports_by_zone[zone].append({
                'code': iata,
                'name': airport_name
            })
        
        return airports_by_zone
        
    except Exception as e:
        print(f"Error loading airport data: {e}")
        return {}

if __name__ == "__main__":
    # Test loading
    mapping = load_airport_mapping()
    print(f"\nLoaded {len(mapping)} airports")
    print("\nSample mappings:")
    for i, (airport, zone) in enumerate(list(mapping.items())[:10]):
        print(f"  {airport} -> {zone}")
