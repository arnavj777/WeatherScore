# Airport Search & Weather App

A modern web application that allows users to search for airports from a curated database, view them on an interactive Google Map, and get detailed information for selected airports.

## Features

- **Curated Airport Database**: 76+ airports across 5 US regions (Northeast, Pacific Coast, Rocky Mountains, Central Plains, Southeast)
- **Smart Search**: Search by IATA code, airport name, city, state, or region
- **Interactive Map**: Google Maps integration with clickable airport markers
- **Airport Details**: Comprehensive information about selected airports
- **Weather Data**: Real-time weather information (with graceful fallback for missing API key)
- **Responsive Design**: Works on desktop and mobile devices

## Quick Start

### Option 1: Easy Startup (Recommended)

1. **Get a Google Maps API key** (required for map display):

   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Enable "Maps JavaScript API"
   - Create an API key
   - Update `frontend/src/App.jsx` line 16 with your key

2. **Run the application**:
   ```bash
   ./start_app.sh
   ```

This will start both the backend and frontend servers automatically.

### Option 2: Manual Setup

#### Prerequisites

- Python 3.7+
- Node.js 16+
- Google Maps API key (required)
- OpenWeatherMap API key (optional - app works without it)

#### Backend Setup

1. Navigate to the source directory:

   ```bash
   cd source
   ```

2. Install Python dependencies:

   ```bash
   pip install flask flask-cors requests
   ```

3. (Optional) Add OpenWeatherMap API key in `main.py`:

   - Replace `'your_openweathermap_api_key'` with your OpenWeatherMap API key
   - If not provided, the app will show mock weather data

4. Run the Flask server:
   ```bash
   python main.py
   ```

#### Frontend Setup

1. Navigate to the frontend directory:

   ```bash
   cd frontend
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Add your Google Maps API key in `src/App.jsx`:

   - Replace `'YOUR_GOOGLE_MAPS_API_KEY'` with your actual Google Maps API key

4. Start the development server:
   ```bash
   npm run dev
   ```

## Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8080

## Airport Database

The app includes 76+ airports across 5 US regions:

### Northeast (12 airports)

BOS, JFK, LGA, EWR, PHL, BWI, IAD, DCA, PWM, BTV, ALB, SYR

### Pacific Coast (16 airports)

LAX, SEA, SFO, SAN, LAS, PDX, SNA, SJC, SMF, BUR, OAK, BFL, EUG, RDM, SPD, VGT

### Rocky Mountains (12 airports)

DEN, SLC, ABQ, PHX, BOI, BZN, BIL, COS, BUF, ASE, TUS, FAT

### Central Plains (16 airports)

ORD, OKC, DFW, IAH, MSP, STL, MCI, ICT, AUS, SAT, HOU, DAL, LNK, OMA, DSM, FAR

### Southeast (20 airports)

ATL, MIA, CLT, MCO, TPA, FLL, BNA, RDU, JAX, RSW, MSY, SAV, CHS, GSP, CHA, TLH, GNV, MKY, PNS

## Search Examples

- **IATA Codes**: "JFK", "LAX", "ORD"
- **Cities**: "Los Angeles", "Chicago", "Miami"
- **States**: "California", "New York", "Florida"
- **Regions**: "Northeast", "PacificCoast", "Southeast"

## API Endpoints

### Backend Endpoints

- `GET /api/weather/airport?lat={lat}&lng={lng}` - Get weather data for coordinates
- `GET /api/weather` - Get US weather data

## Technologies Used

### Backend

- Python Flask
- Flask-CORS for cross-origin requests
- Requests for API calls
- OpenWeatherMap API for weather data (optional)

### Frontend

- React 19
- Google Maps JavaScript API
- Axios for HTTP requests
- Modern CSS with Flexbox and Grid

## Configuration

### Google Maps API (Required)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Enable the Maps JavaScript API
3. Create an API key
4. Update the key in `frontend/src/App.jsx`

### OpenWeatherMap API (Optional)

1. Sign up at [OpenWeatherMap](https://openweathermap.org/api)
2. Get your free API key
3. Update the key in `source/main.py`
4. If not provided, mock weather data will be shown

## Troubleshooting

### Common Issues

1. **Google Maps not loading**: Check your API key and ensure Maps JavaScript API is enabled
2. **Weather shows mock data**: This is normal if you haven't added an OpenWeatherMap API key
3. **CORS errors**: Ensure Flask-CORS is properly configured
4. **Port conflicts**: Make sure ports 8080 and 5173 are available

### Debug Mode

Both servers run in debug mode by default. Check the console for error messages and API responses.

## License

This project is open source and available under the MIT License.
