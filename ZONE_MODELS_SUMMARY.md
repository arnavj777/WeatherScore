# Zone Models Summary

## Overview

You have **5 separate XGBoost models** trained for different US geographic zones. Each model is trained on region-specific weather data and actual flight delay records.

## Available Zone Models

| Zone | Airports | Model Status | Test R² |
|------|----------|--------------|---------|
| **Northeast** | BOS, JFK | ✅ Trained | 0.116 |
| **PacificCoast** | LAX, SEA | ✅ Trained | 0.053 |
| **RockyMountains** | DEN | ✅ Trained | 0.103 |
| **CentralPlains** | ORD, OKC | ✅ Trained | 0.118 |
| **Southeast** | ATL, MIA | ✅ Trained | 0.298 |

## Model Files Location

All models are saved in: `models/zones/`

Each zone has 3 files:
- `{ZoneName}_model.pkl` - Trained XGBoost model
- `{ZoneName}_scaler.pkl` - Feature scaler
- `{ZoneName}_features.txt` - List of features used

## How to Use Individual Zone Models

### Python Code

```python
from Src.predict_zone_risk import predict_zone_risk, interpret_risk_score

# Define weather conditions
weather = {
    'temperature_c': 15.0,
    'dewpoint_c': 10.0,
    'wind_direction': 270,
    'wind_speed_kts': 10.0,
    'gust': 12.0,
    'visibility_km': 10.0,
    'ceiling_ft': 5000.0,
    'sea_level_pressure_mb': 1013.25,
    'relh': 65.0,
    'temp_spread': 5.0,
    'gust_factor': 1.2,
    'ceiling_vis_ratio': 2.0,
    'pressure_change': 0.0,
    'humidity': 65.0,
    'hour': 12,
    'month': 6,
    'is_night': 0,
    'departure_hour': 12
}

# Predict for specific zone
risk_score = predict_zone_risk('Northeast', weather)
category = interpret_risk_score(risk_score[0])

print(f"Northeast Risk: {risk_score[0]:.1f}/100 - {category}")
```

### Command Line

```bash
# Test all zone models
python Src\test_all_zone_models.py

# Test specific zone
python Src\predict_zone_risk.py
```

## Model Characteristics

### Northeast (BOS, JFK)
- **R²**: 0.116
- **Key Features**: Wind direction, visibility, ceiling
- **Use Case**: Boston and New York metropolitan areas

### PacificCoast (LAX, SEA)
- **R²**: 0.053
- **Key Features**: Dewpoint, humidity, ceiling
- **Use Case**: West Coast airports (Los Angeles, Seattle)

### RockyMountains (DEN)
- **R²**: 0.103
- **Key Features**: Humidity, ceiling, night operations
- **Use Case**: High-altitude Denver airport

### CentralPlains (ORD, OKC)
- **R²**: 0.118
- **Key Features**: Humidity, ceiling, time of day
- **Use Case**: Midwest/Plains region airports

### Southeast (ATL, MIA)
- **R²**: 0.298 (Best performing model)
- **Key Features**: **Visibility** (37% importance)
- **Use Case**: Southeast US, highest weather impact

## Why Separate Models?

Each zone has:
- **Different weather patterns**: Regional climate differences
- **Different airport characteristics**: Elevation, typical wind patterns
- **Different operational contexts**: Regional airspace considerations
- **Better performance**: Zone-specific models capture regional nuances

## Testing Results

All models successfully tested with sample weather data:

```
✅ Northeast - Score: 3.6/100 (Good weather)
✅ PacificCoast - Score: 2.2/100 (Good weather)
✅ RockyMountains - Score: 1.7/100 (Good weather)
✅ CentralPlains - Score: 0.0/100 (Good weather)
✅ Southeast - Score: 4.3/100 (Good weather)
```

## Required Features

All models expect these weather features:

### Weather Parameters
- `temperature_c` - Temperature in Celsius
- `dewpoint_c` - Dewpoint in Celsius
- `wind_direction` - Wind direction (degrees)
- `wind_speed_kts` - Wind speed (knots)
- `gust` - Wind gust speed (knots)
- `visibility_km` - Visibility (kilometers)
- `ceiling_ft` - Ceiling height (feet)
- `sea_level_pressure_mb` - Sea level pressure (millibars)
- `relh` - Relative humidity (%)

### Engineered Features
- `temp_spread` - Temperature minus dewpoint
- `gust_factor` - Gust / wind speed ratio
- `ceiling_vis_ratio` - Ceiling to visibility ratio
- `pressure_change` - Change in pressure
- `humidity` - Humidity percentage
- `hour` - Hour of day (0-23)
- `month` - Month (1-12)
- `is_night` - Binary (0=day, 1=night)
- `departure_hour` - Departure hour (0-23)

## Model Training Details

All models were trained with:
- **Algorithm**: XGBoost Regressor
- **Hyperparameters**:
  - `n_estimators=300`
  - `max_depth=8`
  - `learning_rate=0.05`
  - `min_child_weight=2`
  - `subsample=0.9`
  - `colsample_bytree=0.9`
  - `gamma=0.1`
- **Feature Scaling**: StandardScaler
- **Feature Selection**: VarianceThreshold (removes low-variance features)
- **Training Data**: January 2025 weather + flight delay data
- **Test Size**: 20% holdout

## Performance Interpretation

R² scores of 0.05-0.30 are **normal and expected** for weather-focused flight risk models because:
- Weather explains only a fraction of flight delays
- Most delays are non-weather (ATC congestion, maintenance, etc.)
- This is consistent with aviation research

The **Southeast model performs best** (R² = 0.30) because:
- Southeast experiences more significant weather events
- Weather has stronger operational impact in this region
- Visibility is the most important feature (37% importance)

## Summary

✅ **All 5 zone models are trained and operational**
✅ **Each zone has its own XGBoost model tailored to regional patterns**
✅ **Models can predict weather-related flight risk (0-100 scale)**
✅ **Southeast model shows strongest weather signal**

For more details on model performance, see `MODEL_EXPLANATION.md`
