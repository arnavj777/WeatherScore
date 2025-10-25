# XGBoost Flight Risk Integration Guide

This guide explains how the XGBoost flight risk model has been integrated into the TidalHack frontend application.

## Overview

The integration connects your trained XGBoost models to the TidalHack airport search interface, providing real-time flight risk predictions based on current weather conditions from NOAA METAR data.

## Architecture

```
Frontend (React) 
    ↓ HTTP Request
Backend API (Flask)
    ↓ Python Import
WeatherScores Project
    ↓ Model Loading
XGBoost Models (5 regional models)
```

## What Was Integrated

### 1. Backend API (`source/main.py`)
- Added `/api/flight-risk` endpoint
- Fetches real-time METAR data from NOAA
- Routes to appropriate zone model (Northeast, PacificCoast, RockyMountains, CentralPlains, Southeast)
- Returns risk score, category, and weather details

### 2. Frontend Display (`frontend/src/App.jsx`)
- Added "Flight Risk Assessment" section
- Displays risk score (0-100) with color-coded badge
- Shows risk category and detailed assessment
- Includes METAR weather data used for prediction

### 3. Styling (`frontend/src/App.css`)
- Color-coded risk levels (green → yellow → orange → red)
- Gradient backgrounds for visual impact
- Responsive design

## How to Use

### Starting the Application

1. **Start Backend Server:**
   ```bash
   cd C:\Users\arnav\Downloads\TidalHack-main\TidalHack-main
   python source/main.py
   ```
   Server runs on `http://localhost:8080`

2. **Start Frontend:**
   ```bash
   cd frontend
   npm install  # First time only
   npm run dev
   ```
   Frontend runs on `http://localhost:5173` (or similar)

### Using the Application

1. **Search for an airport** (e.g., "LAX", "JFK", "ORD")
2. **Click on any airport** in the results
3. **View the Flight Risk Assessment** section which shows:
   - Risk Score (0-100)
   - Risk Category (Very Low, Low, Moderate, High, Very High)
   - Regional Model used
   - Detailed Assessment
   - METAR Weather Data

## Supported Airports

The integration supports all airports in your Excel file across 5 regions:

- **Northeast**: BOS, JFK, LGA, EWR, PHL, BWI, IAD, DCA, PWM, BTV, ALB, SYR
- **PacificCoast**: LAX, SEA, SFO, SAN, LAS, PDX, SNA, SJC, SMF, BUR, OAK, BFL, EUG, RDM, SPD, VGT
- **RockyMountains**: DEN, SLC, ABQ, PHX, BOI, BZN, BIL, COS, BUF, ASE, TUS, FAT
- **CentralPlains**: ORD, OKC, DFW, IAH, MSP, STL, MCI, ICT, AUS, SAT, HOU, DAL, LNK, OMA, DSM, FAR
- **Southeast**: ATL, MIA, CLT, MCO, TPA, FLL, BNA, RDU, JAX, RSW, MSY, SAV, CHS, GSP, CHA, TLH, GNV, MKY, PNS

## Data Flow

```
User clicks airport
    ↓
Frontend: selectAirport(airport)
    ↓
API Call: GET /api/flight-risk?iata=AUS
    ↓
Backend: get_flight_risk()
    ↓
airport_code_to_icao('AUS') → 'KAUS'
    ↓
fetch_metar_data('KAUS')
    ↓
NOAA API → Raw METAR text
    ↓
parse_metar_text() → Weather dict
    ↓
predict_zone_risk('CentralPlains', weather_data)
    ↓
Load model: models/zones/CentralPlains/model.pkl
    ↓
XGBoost prediction → Risk score
    ↓
Return JSON to frontend
    ↓
Display in "Flight Risk Assessment" section
```

## Features

### Real-Time Weather
- Fetches current METAR data from NOAA Aviation Weather API
- Updates risk predictions based on live conditions

### Zone-Specific Models
- Each US region has its own trained model
- Optimized for regional weather patterns

### Visual Risk Display
- **Green (0-20)**: Very Low Risk
- **Yellow (20-60)**: Low-Moderate Risk
- **Orange (60-80)**: High Risk
- **Red (80-100)**: Very High Risk

### Detailed Information
- Risk score and category
- Regional model used
- Current weather conditions (METAR)
- AI-powered assessment

## Troubleshooting

### Model Not Available
```
Error: XGBoost model not available
```
**Solution**: Ensure the WeatherScores path is correct in `source/main.py`
```python
sys.path.append(r'C:\Arnav\TAMU\WeatherScores')
```

### METAR Data Unavailable
```
Error: Failed to fetch METAR data
```
**Solution**: Check internet connection or API availability

### Airport Not Found
```
Error: Airport XXX not found in any zone
```
**Solution**: Airport not in supported list. Add to zone_map in backend.

## Future Enhancements

- Historical risk trends
- Multi-airport comparison
- Alert notifications for high-risk conditions
- Export predictions to PDF
- Integration with flight scheduling systems

## Technical Details

### Risk Score Interpretation
- **0-20**: Excellent weather - Normal operations
- **20-40**: Good weather - Minor concerns
- **40-60**: Moderate concerns - Possible delays
- **60-80**: Significant issues - Delays likely
- **80-100**: Dangerous conditions - Cancellations possible

### Model Performance
See `MODEL_TESTING_RESULTS.md` for detailed performance metrics by zone.

### API Endpoints
- `GET /api/flight-risk?iata=AUS` - Get flight risk prediction
- Returns: JSON with risk score, category, weather data, and interpretation
