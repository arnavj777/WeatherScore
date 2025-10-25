#!/bin/bash

echo "🚀 Starting Airport Search & Weather App"
echo "========================================"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python3 first."
    exit 1
fi

# Check if Node.js is available
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Check if npm is available
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm first."
    exit 1
fi

echo "✅ Prerequisites check passed"
echo ""

# Start backend server
echo "🔧 Starting Flask backend server..."
cd /Users/yogansh.agarwal/Documents/GitHub/WeatherScore
source venv/bin/activate
cd TidalHack-main/source
python3 main.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 2

# Start frontend server
echo "🎨 Starting React frontend server..."
cd /Users/yogansh.agarwal/Documents/GitHub/WeatherScore/TidalHack-main/frontend
npm run dev &
FRONTEND_PID=$!

echo ""
echo "🎉 Both servers are starting up!"
echo ""
echo "📍 Backend API: http://localhost:8080"
echo "🌐 Frontend App: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop both servers"

# Function to cleanup processes on exit
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ Servers stopped"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Wait for processes
wait
