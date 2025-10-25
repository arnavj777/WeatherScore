# Airport Integration with Excel File

## Overview

The system now loads airport data from `Data/international_airports_by_region.xlsx` and automatically maps airports to their zones.

## Excel File Structure

The Excel file (`Data/international_airports_by_region.xlsx`) contains:

| Column | Description |
|--------|-------------|
| Airport Name | Full name of the airport |
| IATA | 3-letter airport code (e.g., LAX, JFK) |
| City | City name |
| State | State abbreviation |
| Region | Regional classification |

## Supported Regions

The Excel file maps to these zones:

- `pacificcoast` → PacificCoast
- `northeast` → Northeast  
- `centralplains` → CentralPlains
- `rockymountains` → RockyMountains
- Other regions → Southeast (default)

## Current Airport Count

**34 airports** loaded from the Excel file, distributed across zones:

- PacificCoast: 8 airports (LAX, SFO, SEA, PDX, SAN, OAK, SJC, SMF)
- Northeast: 12 airports (JFK, LGA, EWR, BOS, BWI, PHL, IAD, BDL, BUF, ALB, PVD, PWM)
- CentralPlains: 6 airports (MCI, OMA, DSM, STL, TUL, ICT)
- RockyMountains: 8 airports (DEN, SLC, BOI, BIL, BZN, JAC, COS, MSO)

## How It Works

### 1. Loading Airports
```python
from Src.load_airports import load_airport_mapping

# Load all airports from Excel
airports = load_airport_mapping()
# Returns: {'LAX': 'PacificCoast', 'JFK': 'Northeast', ...}
```

### 2. Using in Interactive Tool
The `interactive_test.py` automatically:
1. Loads airports from Excel on startup
2. Maps any entered airport code to its zone
3. Uses the appropriate regional model

### 3. Adding More Airports

Simply add rows to the Excel file:

| Airport Name | IATA | City | State | Region |
|--------------|------|------|-------|--------|
| New Airport | XXX | City | XX | regionname |

The system will automatically include them on next run.

## Files Involved

- `Data/international_airports_by_region.xlsx` - Airport data source
- `Src/load_airports.py` - Loader functions
- `interactive_test.py` - Uses loaded airports

## Testing

Test the loading:
```bash
python Src\load_airports.py
```

Test with interactive tool:
```bash
python interactive_test.py
# Enter any airport from the Excel file
```

## Benefits

1. **Easy to update**: Just edit the Excel file
2. **Centralized data**: All airports in one place
3. **Automatic mapping**: No code changes needed
4. **Extensible**: Add unlimited airports

## Example Airports by Zone

### PacificCoast (8 airports)
- LAX - Los Angeles International Airport
- SFO - San Francisco International Airport
- SEA - Seattle-Tacoma International Airport
- PDX - Portland International Airport
- SAN - San Diego International Airport
- OAK - Oakland International Airport
- SJC - San Jose International Airport
- SMF - Sacramento International Airport

### Northeast (12 airports)
- JFK - John F. Kennedy International Airport
- LGA - LaGuardia Airport
- EWR - Newark Liberty International Airport
- BOS - Boston Logan International Airport
- BWI - Baltimore/Washington International Airport
- PHL - Philadelphia International Airport
- IAD - Washington Dulles International Airport
- BDL - Bradley International Airport
- BUF - Buffalo Niagara International Airport
- ALB - Albany International Airport
- PVD - T.F. Green Airport (Providence)
- PWM - Portland International Jetport

### RockyMountains (8 airports)
- DEN - Denver International Airport
- SLC - Salt Lake City International Airport
- BOI - Boise Airport
- BIL - Billings Logan International Airport
- BZN - Bozeman Yellowstone International Airport
- JAC - Jackson Hole Airport
- COS - Colorado Springs Airport
- MSO - Missoula Montana Airport

### CentralPlains (6 airports)
- MCI - Kansas City International Airport
- OMA - Eppley Airfield (Omaha)
- DSM - Des Moines International Airport
- STL - St. Louis Lambert International Airport
- TUL - Tulsa International Airport
- ICT - Wichita Dwight D. Eisenhower National Airport
