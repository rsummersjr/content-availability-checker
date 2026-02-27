#!/bin/bash

# Music Track Finder - Stop Server Script

echo "🛑 Stopping Music Track Finder server..."
echo ""

# Find the process using port 5001
PID=$(lsof -ti:5001)

if [ -z "$PID" ]; then
    echo "ℹ️  No server running on port 5001"
    exit 0
fi

# Kill the process
kill $PID 2>/dev/null

# Wait a moment
sleep 1

# Check if it's still running
if lsof -Pi :5001 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "⚠️  Server still running, forcing shutdown..."
    kill -9 $PID 2>/dev/null
    sleep 1
fi

# Verify it stopped
if ! lsof -Pi :5001 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "✅ Server stopped successfully"
else
    echo "❌ Failed to stop server"
    exit 1
fi
