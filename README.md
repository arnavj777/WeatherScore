# Flight Risk Scoring System

A machine learning system that uses XGBoost to predict flight risk scores (0-100) based on weather conditions for multiple US geographic zones. The system analyzes METAR weather data and airport observations integrated with actual flight delay data to assess weather-related flight risks across 5 major US regions.

## Features

- **Real-Time METAR Integration**: Fetch current weather data directly from NOAA Aviation Weather API
- **Automated Data Processing**: Parses METAR format weather data and combines it with airport observations
- **Machine Learning Model**: XGBoost-based regression model for accurate risk prediction
- **0-100 Risk Scoring**: Simple scoring system where 100 = maximum flight risk
- **Multi-Zone Support**: 5 regional models covering all US airports
- **Comprehensive Feature Engineering**: Uses multiple weather parameters including visibility, ceiling, wind speed, and more
- **34+ Airport Support**: Loads airports from Excel file for easy expansion

## Installation

1. Create and activate a virtual environment:
```bash
python -m venv myenv
myenv\Scripts\activate  # Windows
source myenv/bin/activate  # Linux/Mac
```

2. Install required packages:
```bash
pip install pandas numpy xgboost scikit-learn joblib
```

## Data Processing

The system processes two main data sources:
- **METAR Data** (`4152601.csv`): Standard weather observations in METAR format
- **Airport Data** (`AUS.csv`): Austin Bergstrom International Airport weather observations

### Processing Steps

1. Parse METAR format fields (temperature, wind, visibility, ceiling, pressure)
2. Convert units and handle missing values
3. Combine datasets by date
4. Engineer additional features (temp spread, gust factor, ceiling/visibility ratio, etc.)

### Running Data Processing

```bash
python Src\data_processing.py
```

This creates `Data/cleaned_weather_data.csv` with processed data.

## Model Training

The model uses the following key features:

### Weather Parameters
- Temperature (°C)
- Dewpoint (°C)
- Wind direction and speed (knots)
- Visibility (km)
- Ceiling height (feet)
- Sea level pressure (mb)
- Wind gusts
- Relative humidity

### Engineered Features
- Temperature spread (temp - dewpoint)
- Gust factor (gust / wind speed)
- Ceiling to visibility ratio
- Pressure changes
- Time features (hour, month, day/night)

### Risk Scoring Methodology

The baseline risk score is calculated from:
- **Visibility** (0-40 points): Lower visibility = higher risk
- **Ceiling** (0-30 points): Lower ceiling = higher risk  
- **Wind Speed** (0-20 points): Higher winds = higher risk
- **Wind Gusts** (0-10 points): Strong gusts = higher risk

### Training the Model

```bash
python Src\model_training.py
```

The model will be saved to `models/` directory:
- `xgboost_flight_risk_model.pkl` - Trained model
- `scaler.pkl` - Feature scaler
- `feature_names.txt` - List of features

## Model Performance

### Multi-Zone Models

The system includes 5 regional models trained on actual flight delay data:

| Zone | Test R² | Test RMSE | Key Features |
|------|---------|-----------|--------------|
| **Northeast** (BOS, JFK) | 0.116 | 5.82 | Wind direction, visibility, ceiling |
| **PacificCoast** (LAX, SEA) | 0.053 | 5.66 | Dewpoint, humidity, ceiling |
| **RockyMountains** (DEN) | 0.103 | 6.34 | Humidity, ceiling, night operations |
| **CentralPlains** (ORD, OKC) | 0.118 | 7.67 | Humidity, ceiling, time of day |
| **Southeast** (ATL, MIA) | **0.298** | 7.94 | **Visibility** (most important) |

**Note on R² scores**: Weather explains a modest fraction of flight delays because many delays stem from non-weather causes (ATC congestion, maintenance, cascading delays). An R² around 0.1–0.3 is expected for weather-focused flight risk models. The Southeast model captures the strongest weather signal.

## Using the Model

### Basic Usage

```python
from Src.predict_risk import predict_risk, interpret_risk_score

# Define weather conditions
weather = {
    'temperature_c_aus': 15.0,
    'dewpoint_c_aus': 10.0,
    'wind_direction_aus': 270,
    'wind_speed_kts_aus': 5.0,
    'visibility_km_aus': 10.0,
    'ceiling_ft_aus': 5000.0,
    'sea_level_pressure_mb_aus': 1013.0,
    'gust': 0.0,
    'relh': 70.0,
    'temp_spread': 5.0,
    'gust_factor': 0.0,
    'ceiling_vis_ratio': 1.5,
    'pressure_change': 0.0,
    'humidity': 70.0,
    'hour': 12,
    'month': 6,
    'is_night': 0
}

# Predict risk score
risk_score = predict_risk(weather)
category = interpret_risk_score(risk_score[0])

print(f"Risk Score: {risk_score[0]:.1f}/100")
print(f"Category: {category}")
```

### Command Line Usage

```bash
python Src\predict_risk.py
```

This runs example predictions with sample weather conditions.

### Multi-Zone Prediction

To predict risk for a specific US region:

```python
from Src.predict_zone_risk import predict_zone_risk

# Define weather conditions for a specific zone
weather = {
    'temperature_c': 20.0,
    'dewpoint_c': 15.0,
    'wind_direction': 270,
    'wind_speed_kts': 15.0,
    # ... all required features
}

# Predict for Northeast
risk_score = predict_zone_risk('Northeast', weather)
```

Available zones: `Northeast`, `PacificCoast`, `RockyMountains`, `CentralPlains`, `Southeast`

### Interactive Testing

**Option 1: Interactive Interface with Real-Time METAR**

To test with real-time weather data or custom values:

```bash
python interactive_test.py
```

Features:
- **Real-time METAR fetching** from NOAA API
- Support for 34+ airports from Excel file
- Automatic zone detection and model selection
- Manual weather entry option
- Detailed risk interpretation

**Quick Example:**
```
Enter Airport Code: AUS
Fetch current weather from NOAA METAR? (y/n): y
Fetches current weather automatically!
```

**Option 2: Legacy Interactive Interface**

```bash
python Src\test_model.py
```

This will prompt you to enter weather conditions and provide real-time risk predictions. You can:
- Enter your own values or press Enter to use defaults
- Test multiple scenarios in one session
- See detailed risk breakdowns and recommendations

**Option 2: Programmatic Testing**

Edit and run the example test file to test with your own custom values:

```bash
python Src\example_test.py
```

Edit the weather dictionaries in `Src/example_test.py` to customize the test conditions. This is useful for:
- Batch testing multiple scenarios
- Programmatic integration
- Reproducible test cases

## Risk Score Interpretation

- **0-20**: Very Low Risk
- **20-40**: Low Risk
- **40-60**: Moderate Risk
- **60-80**: High Risk
- **80-100**: Very High Risk

## Example Scenarios

### Good Weather Conditions
- Visibility: 10 km
- Ceiling: 5000 ft
- Wind Speed: 5 knots
- **Risk Score: 4.7** (Very Low Risk)

### Poor Weather Conditions
- Visibility: 0.5 km
- Ceiling: 200 ft
- Wind Speed: 35 knots
- Gusts: 45 knots
- **Risk Score: 99.7** (Very High Risk)

## Project Structure

```
WeatherScores/
├── Data/
│   ├── 4152601.csv          # METAR weather data
│   ├── AUS.csv              # Airport weather data
│   └── cleaned_weather_data.csv  # Processed data
├── Src/
│   ├── data_processing.py   # Data cleaning and processing
│   ├── model_training.py    # Model training
│   └── predict_risk.py      # Risk prediction
├── models/                   # Saved models
│   ├── xgboost_flight_risk_model.pkl
│   ├── scaler.pkl
│   └── feature_names.txt
└── README.md
```

## Requirements

- Python 3.7+
- pandas
- numpy
- xgboost
- scikit-learn
- joblib

## License

This project is for educational and research purposes.

## Notes

- The model was trained on Austin Bergstrom International Airport weather data
- Risk scores are estimates based on historical weather patterns
- Always consult with aviation professionals for actual flight decisions
- Weather conditions can change rapidly; real-time monitoring is essential for flight safety
