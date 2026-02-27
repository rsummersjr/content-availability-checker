#!/bin/bash

echo "🎵 Music Track Finder - Starting application..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo ""
    echo "⚠️  Warning: .env file not found"
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo ""
    echo "📝 Please edit the .env file and add your API keys:"
    echo "   - YOUTUBE_API_KEY (recommended for YouTube/YouTube Music)"
    echo "   - APPLE_MUSIC_API_KEY (optional)"
    echo ""
    echo "Note: Deezer works without API keys!"
    echo ""
fi

# Start the application
echo ""
echo "🚀 Starting Flask server..."
echo "📱 Open your browser and navigate to: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python app.py
