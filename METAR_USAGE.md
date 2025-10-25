# Real-Time METAR Data Integration

## Overview

The system now supports fetching **real-time weather data** from the NOAA Aviation Weather API using METAR (Meteorological Aerodrome Report) data.

## How It Works

1. **User enters airport code** (e.g., AUS, LAX, JFK)
2. **System fetches current METAR** from NOAA API
3. **METAR parsed** into structured weather data
4. **Flight risk score calculated** using the regional model

## Usage

### Interactive Tool

```bash
python interactive_test.py
```

When prompted:
1. Enter airport code (e.g., `AUS`)
2. Choose **"y"** when asked to fetch from NOAA METAR
3. System automatically fetches current weather and calculates risk

### Example Session

```
Enter Airport Code: AUS
✓ AUS is in the CentralPlains zone

Fetch current weather from NOAA METAR? (y/n): y

Fetching current METAR data...
METAR: METAR KAUS 251953Z 20003KT 10SM FEW060 OVC110 22/18 A2989

✅ Successfully fetched METAR data!

Weather Conditions:
  Temperature: 22.0°C
  Wind: 3.0 kts from 200°
  Visibility: 16.1 km
  Ceiling: 11000 ft

🟢 FLIGHT RISK SCORE: 15.3/100 - Very Low Risk
```

## METAR Data Parsed

The system extracts:
- ✅ **Temperature** (from METAR temp field)
- ✅ **Dewpoint** (from METAR dewpoint field)
- ✅ **Wind Direction & Speed** (from wind field)
- ✅ **Wind Gusts** (from G in wind field)
- ✅ **Visibility** (from visibility field)
- ✅ **Cloud Ceiling** (from cloud layer)
- ✅ **Pressure** (from altimeter setting)
- ✅ **Relative Humidity** (calculated from temp/dewpoint)

Plus derived features:
- Temperature spread
- Gust factor
- Ceiling/visibility ratio

## Airport Code Conversion

The system automatically converts:
- **IATA codes** (3-letter, e.g., `AUS`) → **ICAO codes** (4-letter, e.g., `KAUS`)
- US airports: Prefix with `K`
- International: Mapped to appropriate ICAO codes

## API Endpoint

Uses: `https://aviationweather.gov/api/data/metar?ids={ICAO}&format=xml`

## Benefits

1. **Real-time data** - Current weather conditions
2. **Accurate** - Official aviation weather data
3. **Automatic** - No manual entry needed
4. **Reliable** - Direct from NOAA source

## Examples

### Austin (AUS)
- Fetches from KAUS (Austin-Bergstrom)
- Uses CentralPlains zone model

### Los Angeles (LAX)
- Fetches from KLAX
- Uses PacificCoast zone model

### New York (JFK)
- Fetches from KJFK
- Uses Northeast zone model

## Troubleshooting

### "No METAR data found"
- Airport may not have METAR reporting
- Try a different major airport
- Fall back to manual entry

### Network timeout
- Check internet connection
- API may be temporarily unavailable
- Retry or use manual entry

## Code Structure

- `Src/fetch_metar.py` - METAR fetching and parsing
- `Src/fetch_metar.fetch_metar_data()` - Fetches from NOAA API
- `Src/fetch_metar.parse_metar_text()` - Parses METAR string
- `Src/fetch_metar.airport_code_to_icao()` - Converts IATA to ICAO

## Testing

Test METAR fetching:
```bash
cd Src
python fetch_metar.py
```

This tests with Austin (KAUS) and displays parsed data.

## Future Enhancements

- Support for TAF (Terminal Aerodrome Forecast) - weather forecasts
- Historical METAR data
- Multiple airport comparison
- Weather trend analysis
