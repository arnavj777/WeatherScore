# Interactive Weather Risk Tester

## Quick Start

```bash
python interactive_test.py
```

## What It Does

1. Enter any airport code from the international airports Excel file
2. Enter your weather conditions
3. Get a 0-100 flight risk score

## Supported Airports

**Supports 34+ international airports from `Data/international_airports_by_region.xlsx`!** Including:

- **PacificCoast**: LAX, SFO, SEA, PDX, SAN, OAK, SJC, SMF
- **Northeast**: JFK, LGA, EWR, BOS, BWI, PHL, IAD, BDL, BUF, ALB, PVD, PWM
- **CentralPlains**: MCI, OMA, DSM, STL, TUL, ICT
- **RockyMountains**: DEN, SLC, BOI, BIL, BZN, JAC, COS, MSO

The system:
1. Loads airport data from `Data/international_airports_by_region.xlsx`
2. Automatically maps airport codes to zones
3. Uses the correct regional model for predictions
4. Returns a 0-100 risk score

**To add more airports**: Simply add them to the Excel file!

## Example Session

```
Enter Airport Code: AUS
✓ AUS is in the CentralPlains zone

Enter weather conditions:
  Temperature (°C): 30
  Visibility (km): 1
  Wind Speed (knots): 20
  (Press Enter for defaults on rest)

Result: 🟡 FLIGHT RISK SCORE: 45.2/100 - Moderate Risk
```

## How It Works

- Each airport maps to one of 5 zones based on geographic region
- Each zone has its own trained XGBoost model
- Models are specifically tuned for regional weather patterns
- Same weather = different scores in different zones

## Quick Reference

| Score | Risk Level | Meaning |
|-------|------------|---------|
| 0-20 | 🟢 Very Low | Excellent conditions |
| 20-40 | 🟡 Low | Good conditions |
| 40-60 | 🟠 Moderate | Some concerns |
| 60-80 | 🟠 High | Significant issues |
| 80-100 | 🔴 Very High | Dangerous conditions |

## Tips

- **Press Enter** for default values on most fields
- **Temperature and dewpoint** auto-calculate the spread
- **Gust factor** auto-calculates from wind speed and gusts
- **Ceiling/visibility ratio** auto-calculates from ceiling and visibility

## Need More Options?

- See `QUICK_START.md` for detailed examples
- See `TESTING_GUIDE.md` for advanced testing
- See `ZONE_MODELS_SUMMARY.md` for model details
