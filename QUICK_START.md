# Quick Start - Interactive Weather Risk Tester

## How to Use

Run the interactive tester:

```bash
python interactive_test.py
```

## What It Does

1. **Prompts for Airport Code** - Enter one of the supported airports
2. **Prompts for Weather Data** - Enter your weather conditions (or press Enter for defaults)
3. **Outputs Risk Score** - Get a 0-100 flight risk score

## Supported Airports

**All major US airports are supported!** Examples include:

| Zone | Example Airports |
|------|------------------|
| **Northeast** | BOS, JFK, LGA, EWR, PHL, BWI, IAD, DCA |
| **Pacific Coast** | LAX, SEA, SFO, SAN, LAS, PDX, SNA, SJC |
| **Rocky Mountains** | DEN, SLC, ABQ, PHX, BOI, TUS, ASE |
| **Central Plains** | **AUS**, ORD, OKC, DFW, IAH, MSP, STL, MCI |
| **Southeast** | ATL, MIA, CLT, MCO, TPA, FLL, BNA, JAX |

The system automatically maps any airport code to its zone and uses the appropriate model.

## Example Usage

### Scenario 1: Good Weather (Press Enter for all defaults)
```
Enter Airport Code: JFK

(Press Enter for all defaults)

Output: FLIGHT RISK SCORE: 3.6/100 - Very Low Risk 🟢
```

### Scenario 2: Poor Visibility
```
Enter Airport Code: ATL
Temperature (°C): 15
Wind Speed (knots): 10
Visibility (km): 0.5        ← LOW VISIBILITY
Ceiling (feet): 200         ← LOW CEILING

Output: FLIGHT RISK SCORE: 75.2/100 - High Risk 🔴
```

### Scenario 3: High Wind
```
Enter Airport Code: DEN
Temperature (°C): 5
Wind Speed (knots): 35      ← HIGH WIND
Gusts (knots): 45           ← STRONG GUSTS
Visibility (km): 10
Ceiling (feet): 5000

Output: FLIGHT RISK SCORE: 62.1/100 - High Risk 🟠
```

## Understanding the Score

| Score | Risk Level | Meaning |
|-------|------------|---------|
| 0-20 | 🟢 Very Low | Excellent conditions |
| 20-40 | 🟡 Low | Good conditions, minor concerns |
| 40-60 | 🟠 Moderate | Some weather concerns |
| 60-80 | 🟠 High | Significant issues |
| 80-100 | 🔴 Very High | Dangerous conditions |

## What You Can Enter

### Basic Weather (Most Important)
- **Temperature** (°C): e.g., 20
- **Wind Speed** (knots): e.g., 15
- **Visibility** (km): e.g., 10
- **Ceiling** (feet): e.g., 5000
- **Wind Gusts** (knots): e.g., 18

### Advanced (Optional)
- Wind Direction (0-360°)
- Dewpoint (°C)
- Humidity (%)
- Pressure (mb)
- Time of day, month, etc.

**Tip**: For quick tests, just enter the basic weather values and press Enter for the rest!

## Different Zones, Different Sensitivities

The same weather will score differently in different zones:

- **Northeast** (BOS, JFK): Sensitive to wind and visibility
- **PacificCoast** (LAX, SEA): Sensitive to humidity and dewpoint
- **RockyMountains** (DEN): Sensitive to ceiling and night ops
- **CentralPlains** (ORD, OKC): Sensitive to humidity and time
- **Southeast** (ATL, MIA): **Most sensitive to visibility** (best model)

## Quick Test Examples

### Test Good Weather
```bash
python interactive_test.py
# Enter: JFK (or any airport)
# Press Enter for all defaults
# Output: ~0-20 score (🟢)
```

### Test Poor Weather
```bash
python interactive_test.py
# Enter: ATL
# Temperature: 10
# Wind Speed: 30
# Visibility: 0.5
# Ceiling: 200
# (Press Enter for rest)
# Output: 60-100 score (🔴)
```

### Test Moderate Weather
```bash
python interactive_test.py
# Enter: DEN
# Visibility: 2
# Ceiling: 1000
# Wind Speed: 20
# (Press Enter for rest)
# Output: 40-60 score (🟠)
```

## Need Help?

See `TESTING_GUIDE.md` for more detailed documentation.
