# Testing Guide for Flight Risk Models

## Quick Start - 3 Ways to Test

### 1. Quick All-Zone Test (Easiest)
```bash
python Src\test_all_zone_models.py
```
Tests all 5 zone models with default good weather conditions.

### 2. Custom Weather Test (Most Flexible)
```bash
# 1. Edit test_custom_weather.py to change weather conditions
# 2. Run it:
python test_custom_weather.py
```

### 3. Single Zone Example
```bash
python Src\predict_zone_risk.py
```
Shows example usage for Northeast zone.

## Testing Options Explained

### Option 1: Quick Test
**Purpose**: Verify all models work  
**Weather**: Fixed (good conditions)  
**Best for**: Quick verification after setup

```bash
python Src\test_all_zone_models.py
```

### Option 2: Custom Weather Test
**Purpose**: Test your own weather scenarios  
**Weather**: YOU control it (edit the file)  
**Best for**: Testing specific weather conditions

**How to use:**
1. Open `test_custom_weather.py`
2. Modify the `custom_weather` dictionary (lines 9-26)
3. Run: `python test_custom_weather.py`

**Example - Test Poor Weather:**
```python
custom_weather = {
    'temperature_c': 10.0,
    'dewpoint_c': 8.0,
    'wind_direction': 270,
    'wind_speed_kts': 30.0,  # HIGH WIND
    'gust': 45.0,             # STRONG GUSTS
    'visibility_km': 0.5,     # LOW VISIBILITY
    'ceiling_ft': 200.0,      # LOW CEILING
    'sea_level_pressure_mb': 1013.25,
    'relh': 95.0,
    'temp_spread': 2.0,
    'gust_factor': 1.5,
    'ceiling_vis_ratio': 0.13,
    'pressure_change': -2.0,
    'humidity': 95.0,
    'hour': 14,
    'month': 1,
    'is_night': 0,
    'departure_hour': 14
}
```

### Option 3: Interactive Python Shell
**Purpose**: Programmatic testing  
**Best for**: Integration with other code

```python
from Src.predict_zone_risk import predict_zone_risk, interpret_risk_score

# Define weather
weather = {
    'temperature_c': 20.0,
    'dewpoint_c': 15.0,
    'wind_direction': 270,
    'wind_speed_kts': 12.0,
    'gust': 15.0,
    'visibility_km': 10.0,
    'ceiling_ft': 5000.0,
    'sea_level_pressure_mb': 1013.25,
    'relh': 65.0,
    'temp_spread': 5.0,
    'gust_factor': 1.25,
    'ceiling_vis_ratio': 2.0,
    'pressure_change': 0.0,
    'humidity': 65.0,
    'hour': 14,
    'month': 6,
    'is_night': 0,
    'departure_hour': 14
}

# Test specific zone
risk = predict_zone_risk('Southeast', weather)
print(f"Risk: {risk[0]:.1f}/100")
print(f"Category: {interpret_risk_score(risk[0])}")
```

## Understanding Risk Scores

| Score | Category | Meaning |
|-------|----------|---------|
| 0-20 | 🟢 Very Low Risk | Excellent weather conditions |
| 20-40 | 🟡 Low Risk | Good weather, minor concerns |
| 40-60 | 🟠 Moderate Risk | Some weather concerns |
| 60-80 | 🟠 High Risk | Significant weather issues |
| 80-100 | 🔴 Very High Risk | Dangerous weather conditions |

## Test Scenarios

### Good Weather (Low Risk)
```python
{
    'visibility_km': 10.0,
    'ceiling_ft': 5000.0,
    'wind_speed_kts': 10.0,
    'gust': 12.0
}
```
**Expected**: Risk scores 0-20 (🟢)

### Poor Visibility (Moderate Risk)
```python
{
    'visibility_km': 1.0,
    'ceiling_ft': 500.0,
    'wind_speed_kts': 15.0,
    'gust': 18.0
}
```
**Expected**: Risk scores 40-60 (🟠)

### Dangerous Weather (High Risk)
```python
{
    'visibility_km': 0.5,
    'ceiling_ft': 200.0,
    'wind_speed_kts': 35.0,
    'gust': 50.0
}
```
**Expected**: Risk scores 60-100 (🔴)

## Zone-Specific Testing

Each zone reacts differently to weather:

### Northeast (BOS, JFK)
- Sensitive to wind direction and visibility
- Winter weather has strong impact

### PacificCoast (LAX, SEA)
- Dewpoint and humidity matter most
- Coastal fog patterns important

### RockyMountains (DEN)
- Humidity and ceiling most important
- Night operations more sensitive

### CentralPlains (ORD, OKC)
- Humidity and time of day are key
- Seasonal variations strong

### Southeast (ATL, MIA)
- **Visibility is most important (37% weight)**
- Strongest weather signal across all zones
- Best performing model

## Troubleshooting

### "Model files not found" Error
**Solution**: Make sure you're in the project root directory
```bash
cd C:\Arnav\TAMU\WeatherScores
python Src\test_all_zone_models.py
```

### "Missing required feature" Error
**Solution**: Check that all 18 weather features are provided
```python
# Required features:
'temperature_c', 'dewpoint_c', 'wind_direction', 'wind_speed_kts',
'gust', 'visibility_km', 'ceiling_ft', 'sea_level_pressure_mb',
'relh', 'temp_spread', 'gust_factor', 'ceiling_vis_ratio',
'pressure_change', 'humidity', 'hour', 'month', 'is_night',
'departure_hour'
```

### Models Return Same Score
**Solution**: Different zones have different sensitivities - this is normal!

## Quick Test Checklist

- [ ] Run quick test: `python Src\test_all_zone_models.py`
- [ ] All 5 zones return scores
- [ ] Edit `test_custom_weather.py` for your scenario
- [ ] Run custom test: `python test_custom_weather.py`
- [ ] Verify risk scores match weather conditions

## Next Steps

1. **Test with real weather data**: Get METAR data for your airport
2. **Compare zones**: Same weather, different risks by zone
3. **Build scenarios**: Create bad weather, good weather, edge cases
4. **Integrate**: Use models in your own applications

For more details, see:
- `ZONE_MODELS_SUMMARY.md` - Model overview
- `MODEL_EXPLANATION.md` - Why R² scores are what they are
- `README.md` - Full documentation
