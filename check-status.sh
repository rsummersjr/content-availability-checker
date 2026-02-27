#!/bin/bash

# Music Track Finder - Status Checker

echo "🎵 Music Track Finder - Status Check"
echo "======================================"
echo ""

# Check if server is running
if lsof -Pi :5001 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "✅ Server Status: RUNNING"
    echo ""

    # Get process ID
    PID=$(lsof -ti:5001)
    echo "📊 Process ID: $PID"
    echo ""

    echo "🌐 Access URLs:"
    echo "  • http://192.168.86.25:5001"
    echo "  • http://172.21.6.180:5001"
    echo "  • http://127.0.0.1:5001 (local only)"
    echo ""

    # Test the endpoint
    echo "🧪 Testing server response..."
    if curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:5001 | grep -q "200"; then
        echo "✅ Server is responding correctly"
    else
        echo "⚠️  Server is running but may not be responding correctly"
    fi

else
    echo "❌ Server Status: NOT RUNNING"
    echo ""
    echo "To start the server, run: ./start-server.sh"
fi

echo ""
echo "======================================"
