import { useState, useEffect, useRef } from 'react';
import './App.css';
import axios from 'axios';
import { Loader } from '@googlemaps/js-api-loader';

function App() {
  const [searchQuery, setSearchQuery] = useState('');
  const [airports, setAirports] = useState([]);
  const [selectedAirport, setSelectedAirport] = useState(null);
  const [weatherData, setWeatherData] = useState(null);
  const [flightRisk, setFlightRisk] = useState(null);
  const [map, setMap] = useState(null);
  const [markers, setMarkers] = useState([]);
  const mapRef = useRef(null);

  // Google Maps API key - replace with your actual key
  const GOOGLE_MAPS_API_KEY = 'AIzaSyDQi_JrwA-HFSBgKrTx8mmbh08tM447b_s';

  // Helper function to get risk class for styling
  const getRiskClass = (score) => {
    if (score < 20) return 'risk-low';
    if (score < 60) return 'risk-moderate';
    if (score < 80) return 'risk-high';
    return 'risk-very-high';
  };

  // Airport database with regions
  const AIRPORTS_DATABASE = {
    'BOS': { name: 'Logan International Airport', city: 'Boston', state: 'MA', region: 'Northeast', lat: 42.3656, lng: -71.0096 },
    'JFK': { name: 'John F. Kennedy International Airport', city: 'New York', state: 'NY', region: 'Northeast', lat: 40.6413, lng: -73.7781 },
    'LGA': { name: 'LaGuardia Airport', city: 'New York', state: 'NY', region: 'Northeast', lat: 40.7769, lng: -73.8740 },
    'EWR': { name: 'Newark Liberty International Airport', city: 'Newark', state: 'NJ', region: 'Northeast', lat: 40.6895, lng: -74.1745 },
    'PHL': { name: 'Philadelphia International Airport', city: 'Philadelphia', state: 'PA', region: 'Northeast', lat: 39.8729, lng: -75.2437 },
    'BWI': { name: 'Baltimore/Washington International Airport', city: 'Baltimore', state: 'MD', region: 'Northeast', lat: 39.1774, lng: -76.6684 },
    'IAD': { name: 'Washington Dulles International Airport', city: 'Washington', state: 'DC', region: 'Northeast', lat: 38.9531, lng: -77.4565 },
    'DCA': { name: 'Ronald Reagan Washington National Airport', city: 'Washington', state: 'DC', region: 'Northeast', lat: 38.8512, lng: -77.0402 },
    'PWM': { name: 'Portland International Jetport', city: 'Portland', state: 'ME', region: 'Northeast', lat: 43.6462, lng: -70.3093 },
    'BTV': { name: 'Burlington International Airport', city: 'Burlington', state: 'VT', region: 'Northeast', lat: 44.4719, lng: -73.1533 },
    'ALB': { name: 'Albany International Airport', city: 'Albany', state: 'NY', region: 'Northeast', lat: 42.7483, lng: -73.8017 },
    'SYR': { name: 'Syracuse Hancock International Airport', city: 'Syracuse', state: 'NY', region: 'Northeast', lat: 43.1112, lng: -76.1063 },

    'LAX': { name: 'Los Angeles International Airport', city: 'Los Angeles', state: 'CA', region: 'PacificCoast', lat: 33.9416, lng: -118.4085 },
    'SEA': { name: 'Seattle-Tacoma International Airport', city: 'Seattle', state: 'WA', region: 'PacificCoast', lat: 47.4502, lng: -122.3088 },
    'SFO': { name: 'San Francisco International Airport', city: 'San Francisco', state: 'CA', region: 'PacificCoast', lat: 37.6213, lng: -122.3790 },
    'SAN': { name: 'San Diego International Airport', city: 'San Diego', state: 'CA', region: 'PacificCoast', lat: 32.7338, lng: -117.1933 },
    'LAS': { name: 'Harry Reid International Airport', city: 'Las Vegas', state: 'NV', region: 'PacificCoast', lat: 36.0840, lng: -115.1537 },
    'PDX': { name: 'Portland International Airport', city: 'Portland', state: 'OR', region: 'PacificCoast', lat: 45.5898, lng: -122.5951 },
    'SNA': { name: 'John Wayne Airport', city: 'Santa Ana', state: 'CA', region: 'PacificCoast', lat: 33.6757, lng: -117.8682 },
    'SJC': { name: 'San Jose International Airport', city: 'San Jose', state: 'CA', region: 'PacificCoast', lat: 37.3626, lng: -121.9290 },
    'SMF': { name: 'Sacramento International Airport', city: 'Sacramento', state: 'CA', region: 'PacificCoast', lat: 38.6954, lng: -121.5908 },
    'BUR': { name: 'Hollywood Burbank Airport', city: 'Burbank', state: 'CA', region: 'PacificCoast', lat: 34.2006, lng: -118.3587 },
    'OAK': { name: 'Oakland International Airport', city: 'Oakland', state: 'CA', region: 'PacificCoast', lat: 37.8044, lng: -122.2712 },
    'BFL': { name: 'Bakersfield Municipal Airport', city: 'Bakersfield', state: 'CA', region: 'PacificCoast', lat: 35.4339, lng: -119.0568 },
    'EUG': { name: 'Eugene Airport', city: 'Eugene', state: 'OR', region: 'PacificCoast', lat: 44.1246, lng: -123.2120 },
    'RDM': { name: 'Redmond Municipal Airport', city: 'Redmond', state: 'OR', region: 'PacificCoast', lat: 44.2541, lng: -121.1500 },
    'SPD': { name: 'Spokane International Airport', city: 'Spokane', state: 'WA', region: 'PacificCoast', lat: 47.6199, lng: -117.5348 },
    'VGT': { name: 'North Las Vegas Airport', city: 'Las Vegas', state: 'NV', region: 'PacificCoast', lat: 36.2107, lng: -115.1944 },

    'DEN': { name: 'Denver International Airport', city: 'Denver', state: 'CO', region: 'RockyMountains', lat: 39.8561, lng: -104.6737 },
    'SLC': { name: 'Salt Lake City International Airport', city: 'Salt Lake City', state: 'UT', region: 'RockyMountains', lat: 40.7899, lng: -111.9791 },
    'ABQ': { name: 'Albuquerque International Sunport', city: 'Albuquerque', state: 'NM', region: 'RockyMountains', lat: 35.0402, lng: -106.6091 },
    'PHX': { name: 'Phoenix Sky Harbor International Airport', city: 'Phoenix', state: 'AZ', region: 'RockyMountains', lat: 33.4342, lng: -112.0116 },
    'BOI': { name: 'Boise Airport', city: 'Boise', state: 'ID', region: 'RockyMountains', lat: 43.5644, lng: -116.2228 },
    'BZN': { name: 'Bozeman Yellowstone International Airport', city: 'Bozeman', state: 'MT', region: 'RockyMountains', lat: 45.7776, lng: -111.1528 },
    'BIL': { name: 'Billings Logan International Airport', city: 'Billings', state: 'MT', region: 'RockyMountains', lat: 45.8077, lng: -108.5429 },
    'COS': { name: 'Colorado Springs Airport', city: 'Colorado Springs', state: 'CO', region: 'RockyMountains', lat: 38.8058, lng: -104.7008 },
    'BUF': { name: 'Buffalo Niagara International Airport', city: 'Buffalo', state: 'NY', region: 'RockyMountains', lat: 42.9405, lng: -78.7322 },
    'ASE': { name: 'Aspen/Pitkin County Airport', city: 'Aspen', state: 'CO', region: 'RockyMountains', lat: 39.2232, lng: -106.8689 },
    'TUS': { name: 'Tucson International Airport', city: 'Tucson', state: 'AZ', region: 'RockyMountains', lat: 32.1161, lng: -110.9411 },
    'FAT': { name: 'Fresno Yosemite International Airport', city: 'Fresno', state: 'CA', region: 'RockyMountains', lat: 36.7762, lng: -119.7181 },

    'ORD': { name: 'O\'Hare International Airport', city: 'Chicago', state: 'IL', region: 'CentralPlains', lat: 41.9786, lng: -87.9048 },
    'OKC': { name: 'Will Rogers World Airport', city: 'Oklahoma City', state: 'OK', region: 'CentralPlains', lat: 35.3931, lng: -97.6007 },
    'DFW': { name: 'Dallas/Fort Worth International Airport', city: 'Dallas', state: 'TX', region: 'CentralPlains', lat: 32.8968, lng: -97.0380 },
    'IAH': { name: 'George Bush Intercontinental Airport', city: 'Houston', state: 'TX', region: 'CentralPlains', lat: 29.9844, lng: -95.3414 },
    'MSP': { name: 'Minneapolis-Saint Paul International Airport', city: 'Minneapolis', state: 'MN', region: 'CentralPlains', lat: 44.8848, lng: -93.2223 },
    'STL': { name: 'St. Louis Lambert International Airport', city: 'St. Louis', state: 'MO', region: 'CentralPlains', lat: 38.7487, lng: -90.3708 },
    'MCI': { name: 'Kansas City International Airport', city: 'Kansas City', state: 'MO', region: 'CentralPlains', lat: 39.2976, lng: -94.7139 },
    'ICT': { name: 'Wichita Dwight D. Eisenhower National Airport', city: 'Wichita', state: 'KS', region: 'CentralPlains', lat: 37.6499, lng: -97.4331 },
    'AUS': { name: 'Austin-Bergstrom International Airport', city: 'Austin', state: 'TX', region: 'CentralPlains', lat: 30.1945, lng: -97.6699 },
    'SAT': { name: 'San Antonio International Airport', city: 'San Antonio', state: 'TX', region: 'CentralPlains', lat: 29.5337, lng: -98.4698 },
    'HOU': { name: 'William P. Hobby Airport', city: 'Houston', state: 'TX', region: 'CentralPlains', lat: 29.6454, lng: -95.2789 },
    'DAL': { name: 'Dallas Love Field', city: 'Dallas', state: 'TX', region: 'CentralPlains', lat: 32.8471, lng: -96.8518 },
    'LNK': { name: 'Lincoln Airport', city: 'Lincoln', state: 'NE', region: 'CentralPlains', lat: 40.8510, lng: -96.7592 },
    'OMA': { name: 'Eppley Airfield', city: 'Omaha', state: 'NE', region: 'CentralPlains', lat: 41.3025, lng: -95.8942 },
    'DSM': { name: 'Des Moines International Airport', city: 'Des Moines', state: 'IA', region: 'CentralPlains', lat: 41.5340, lng: -93.6631 },
    'FAR': { name: 'Hector International Airport', city: 'Fargo', state: 'ND', region: 'CentralPlains', lat: 46.9207, lng: -96.8158 },

    'ATL': { name: 'Hartsfield-Jackson Atlanta International Airport', city: 'Atlanta', state: 'GA', region: 'Southeast', lat: 33.6407, lng: -84.4277 },
    'MIA': { name: 'Miami International Airport', city: 'Miami', state: 'FL', region: 'Southeast', lat: 25.7959, lng: -80.2870 },
    'CLT': { name: 'Charlotte Douglas International Airport', city: 'Charlotte', state: 'NC', region: 'Southeast', lat: 35.2144, lng: -80.9473 },
    'MCO': { name: 'Orlando International Airport', city: 'Orlando', state: 'FL', region: 'Southeast', lat: 28.4312, lng: -81.3081 },
    'TPA': { name: 'Tampa International Airport', city: 'Tampa', state: 'FL', region: 'Southeast', lat: 27.9755, lng: -82.5332 },
    'FLL': { name: 'Fort Lauderdale-Hollywood International Airport', city: 'Fort Lauderdale', state: 'FL', region: 'Southeast', lat: 26.0726, lng: -80.1527 },
    'BNA': { name: 'Nashville International Airport', city: 'Nashville', state: 'TN', region: 'Southeast', lat: 36.1245, lng: -86.6782 },
    'RDU': { name: 'Raleigh-Durham International Airport', city: 'Raleigh', state: 'NC', region: 'Southeast', lat: 35.8776, lng: -78.7875 },
    'JAX': { name: 'Jacksonville International Airport', city: 'Jacksonville', state: 'FL', region: 'Southeast', lat: 30.4941, lng: -81.6879 },
    'RSW': { name: 'Southwest Florida International Airport', city: 'Fort Myers', state: 'FL', region: 'Southeast', lat: 26.5362, lng: -81.7552 },
    'MSY': { name: 'Louis Armstrong New Orleans International Airport', city: 'New Orleans', state: 'LA', region: 'Southeast', lat: 29.9934, lng: -90.2581 },
    'SAV': { name: 'Savannah/Hilton Head International Airport', city: 'Savannah', state: 'GA', region: 'Southeast', lat: 32.1276, lng: -81.2021 },
    'CHS': { name: 'Charleston International Airport', city: 'Charleston', state: 'SC', region: 'Southeast', lat: 32.8986, lng: -80.0405 },
    'GSP': { name: 'Greenville-Spartanburg International Airport', city: 'Greer', state: 'SC', region: 'Southeast', lat: 34.8957, lng: -82.2189 },
    'CHA': { name: 'Chattanooga Metropolitan Airport', city: 'Chattanooga', state: 'TN', region: 'Southeast', lat: 35.0353, lng: -85.2038 },
    'TLH': { name: 'Tallahassee International Airport', city: 'Tallahassee', state: 'FL', region: 'Southeast', lat: 30.3965, lng: -84.3503 },
    'GNV': { name: 'Gainesville Regional Airport', city: 'Gainesville', state: 'FL', region: 'Southeast', lat: 29.6901, lng: -82.2718 },
    'MKY': { name: 'Marco Island Executive Airport', city: 'Marco Island', state: 'FL', region: 'Southeast', lat: 25.9954, lng: -81.6726 },
    'PNS': { name: 'Pensacola International Airport', city: 'Pensacola', state: 'FL', region: 'Southeast', lat: 30.4734, lng: -87.1866 }
  };

  // Load Google Maps
  useEffect(() => {
    if (GOOGLE_MAPS_API_KEY === 'YOUR_GOOGLE_MAPS_API_KEY') {
      console.warn('Google Maps API key not configured. Please add your API key to src/App.jsx');
      return;
    }

    const loader = new Loader({
      apiKey: GOOGLE_MAPS_API_KEY,
      version: 'weekly',
      libraries: ['places']
    });

    loader.load().then(() => {
      const mapInstance = new window.google.maps.Map(mapRef.current, {
        center: { lat: 39.8283, lng: -98.5795 }, // Center of US
        zoom: 4,
        mapTypeId: 'roadmap'
      });
      setMap(mapInstance);
    }).catch((error) => {
      console.error('Error loading Google Maps:', error);
    });
  }, []);

  // Search airports when query changes
  useEffect(() => {
    if (searchQuery.length > 0) {
      searchAirports(searchQuery);
    } else {
      setAirports([]);
      updateMapMarkers([]);
    }
  }, [searchQuery]);

  const searchAirports = (query) => {
    const searchTerm = query.toLowerCase();
    const results = [];

    // Search through all airports in the database
    Object.entries(AIRPORTS_DATABASE).forEach(([iata, airportData]) => {
      const matches = 
        iata.toLowerCase().includes(searchTerm) ||
        airportData.name.toLowerCase().includes(searchTerm) ||
        airportData.city.toLowerCase().includes(searchTerm) ||
        airportData.state.toLowerCase().includes(searchTerm) ||
        airportData.region.toLowerCase().includes(searchTerm);

      if (matches) {
        results.push({
          id: iata,
          name: airportData.name,
          city: airportData.city,
          state: airportData.state,
          country: 'USA',
          region: airportData.region,
          latitude: airportData.lat,
          longitude: airportData.lng,
          iata: iata,
          icao: `K${iata}`, // Generate ICAO code
          address: `${airportData.city}, ${airportData.state}`
        });
      }
    });

    setAirports(results);
    updateMapMarkers(results);
  };

  const updateMapMarkers = (airportList) => {
    if (!map) return;

    // Clear existing markers
    markers.forEach(marker => marker.setMap(null));

    const newMarkers = airportList.map(airport => {
      const marker = new window.google.maps.Marker({
        position: { lat: airport.latitude, lng: airport.longitude },
        map: map,
        title: airport.name,
        label: airport.iata
      });

      marker.addListener('click', () => {
        selectAirport(airport);
      });

      return marker;
    });

    setMarkers(newMarkers);
  };

  const selectAirport = async (airport) => {
    setSelectedAirport(airport);
    setFlightRisk(null);
    
    // Center map on selected airport
    if (map) {
      map.setCenter({ lat: airport.latitude, lng: airport.longitude });
      map.setZoom(10);
    }

    // Fetch weather data for the selected airport
    try {
      const response = await axios.get(`http://localhost:8080/api/weather/airport`, {
        params: {
          lat: airport.latitude,
          lng: airport.longitude
        }
      });
      setWeatherData(response.data);
    } catch (error) {
      console.error('Error fetching weather data:', error);
      setWeatherData({ error: 'Weather data unavailable' });
    }

    // Fetch flight risk prediction from XGBoost model
    try {
      const riskResponse = await axios.get(`http://localhost:8080/api/flight-risk`, {
        params: {
          iata: airport.iata
        }
      });
      setFlightRisk(riskResponse.data);
    } catch (error) {
      console.error('Error fetching flight risk:', error);
      setFlightRisk({ error: 'Flight risk prediction unavailable' });
    }
  };

  return (
    <div className="app">
      {/* Search Bar */}
      <div className="search-container">
        <input
          type="text"
          placeholder="Search airports by IATA code, name, city, state, or region (e.g., 'JFK', 'Los Angeles', 'Northeast')..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="search-input"
        />
      </div>

      {/* Main Content */}
      <div className="main-content">
        {/* Map Section */}
        <div className="map-section">
          {GOOGLE_MAPS_API_KEY === 'YOUR_GOOGLE_MAPS_API_KEY' ? (
            <div className="map-placeholder">
              <h3>Google Maps Not Configured</h3>
              <p>Please add your Google Maps API key to src/App.jsx to view the interactive map.</p>
              <p>You can still search and select airports using the list below.</p>
            </div>
          ) : (
            <div ref={mapRef} className="map-container"></div>
          )}
        </div>

        {/* Airport Data Section */}
        <div className="data-section">
          {selectedAirport ? (
            <div className="airport-details">
              <h2>{selectedAirport.name}</h2>
              <div className="airport-info">
                <p><strong>IATA Code:</strong> {selectedAirport.iata}</p>
                <p><strong>ICAO Code:</strong> {selectedAirport.icao}</p>
                <p><strong>Location:</strong> {selectedAirport.city}, {selectedAirport.state}</p>
                <p><strong>Coordinates:</strong> {selectedAirport.latitude}, {selectedAirport.longitude}</p>
              </div>

              {/* Weather info moved to Flight Risk Section below */}

              {/* Flight Risk Section with Complete Model Output */}
              {flightRisk && !flightRisk.error && (
                <div className="flight-risk-info">
                  <h3>🛫 AI Flight Risk Assessment</h3>
                  
                  {/* Prominent Risk Score Display */}
                  <div className="risk-score-container">
                    <div className={`risk-score ${getRiskClass(flightRisk.risk_score)}`}>
                      <span className="score-value">{flightRisk.risk_score.toFixed(1)}</span>
                      <span className="score-label">/100</span>
                    </div>
                    <div className="risk-category">
                      <strong>{flightRisk.risk_category}</strong>
                    </div>
                  </div>

                  {/* Assessment Summary */}
                  <div className="risk-assessment">
                    <p className="assessment-text">{flightRisk.interpretation?.description}</p>
                  </div>

                  {/* Regional Model Info */}
                  <div className="model-info">
                    <p><strong>🧠 AI Model:</strong> {flightRisk.zone} Regional Model</p>
                    <p><strong>📊 Training Data:</strong> Flight delay patterns from {flightRisk.zone}</p>
                  </div>
                  
                  {/* Current Weather Conditions (from METAR) */}
                  {flightRisk.weather_data && (
                    <div className="metar-details">
                      <h4>🌤️ Current METAR Weather</h4>
                      <div className="weather-grid">
                        <div className="weather-item">
                          <span className="weather-label">🌡️ Temperature:</span>
                          <span className="weather-value">{flightRisk.weather_data.temperature_c?.toFixed(1)}°C</span>
                        </div>
                        <div className="weather-item">
                          <span className="weather-label">💨 Wind:</span>
                          <span className="weather-value">{flightRisk.weather_data.wind_speed_kts?.toFixed(1)} kts @ {flightRisk.weather_data.wind_direction?.toFixed(0)}°</span>
                        </div>
                        <div className="weather-item">
                          <span className="weather-label">👁️ Visibility:</span>
                          <span className="weather-value">{flightRisk.weather_data.visibility_km?.toFixed(1)} km</span>
                        </div>
                        <div className="weather-item">
                          <span className="weather-label">☁️ Ceiling:</span>
                          <span className="weather-value">{flightRisk.weather_data.ceiling_ft?.toFixed(0)} ft</span>
                        </div>
                        <div className="weather-item">
                          <span className="weather-label">💧 Humidity:</span>
                          <span className="weather-value">{flightRisk.weather_data.humidity?.toFixed(1)}%</span>
                        </div>
                        <div className="weather-item">
                          <span className="weather-label">🌬️ Gusts:</span>
                          <span className="weather-value">{flightRisk.weather_data.gust?.toFixed(1)} kts</span>
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Technical Details */}
                  <div className="technical-details">
                    <h4>🔬 Model Insights</h4>
                    <p><strong>Data Source:</strong> NOAA Aviation Weather API (METAR)</p>
                    <p><strong>Prediction Time:</strong> Real-time analysis</p>
                    <p><strong>Model Type:</strong> XGBoost Gradient Boosting</p>
                  </div>
                </div>
              )}

              {flightRisk && flightRisk.error && (
                <div className="flight-risk-info">
                  <h3>🛫 Flight Risk Assessment</h3>
                  <div className="risk-error">
                    <p>{flightRisk.error}: {flightRisk.message}</p>
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="placeholder">
              <h3>Search for an Airport</h3>
              <p>Type in the search bar above to find airports from our curated database. Search by IATA code, name, city, state, or region.</p>
              <p>Click on any airport marker or card to view detailed information and weather data.</p>
              <div className="search-examples">
                <p><strong>Try searching:</strong></p>
                <p>• "JFK" or "LAX" (IATA codes)</p>
                <p>• "Los Angeles" or "Chicago" (cities)</p>
                <p>• "Northeast" or "PacificCoast" (regions)</p>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Airport List */}
      <div className="airport-list">
        <h3>Search Results</h3>
        <div className="airport-grid">
          {airports.length > 0 ? (
            airports.map((airport) => (
              <div
                key={airport.id}
                className={`airport-card ${selectedAirport?.id === airport.id ? 'selected' : ''}`}
                onClick={() => selectAirport(airport)}
              >
                <h4>{airport.name}</h4>
                <p>{airport.iata} - {airport.city}, {airport.state}</p>
                <p className="region">{airport.region}</p>
                {airport.address && <p className="address">{airport.address}</p>}
              </div>
            ))
          ) : (
            <div className="no-results">
              <p>No airports found. Try searching for airport names, cities, or IATA codes.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
