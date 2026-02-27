#!/bin/bash

# Music Track Finder - Server Management Script

echo "🎵 Music Track Finder - Server Manager"
echo "======================================"
echo ""

# Check if server is already running
if lsof -Pi :5001 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "⚠️  Server is already running on port 5001"
    echo ""
    echo "Access URLs:"
    echo "  • http://192.168.86.25:5001"
    echo "  • http://172.21.6.180:5001"
    echo "  • http://127.0.0.1:5001 (local only)"
    echo ""
    echo "To stop the server, run: ./stop-server.sh"
    exit 0
fi

# Navigate to the correct directory
cd "$(dirname "$0")"

echo "📍 Working directory: $(pwd)"
echo ""

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ Error: .env file not found!"
    echo "Please make sure your YouTube API key is configured."
    exit 1
fi

echo "✅ Environment file found"
echo ""

# Check if virtual environment exists, create if not
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
    echo ""
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

echo ""
echo "🚀 Starting server..."
echo ""
echo "Access URLs (share with your team):"
echo "  • http://192.168.86.25:5001"
echo "  • http://172.21.6.180:5001"
echo "  • http://127.0.0.1:5001 (local only)"
echo ""
echo "Press Ctrl+C to stop the server"
echo "======================================"
echo ""

# Start the Flask app
python3 app.py
