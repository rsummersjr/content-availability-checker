#!/bin/bash

# Music Track Finder - Heroku Deployment Script

echo "🚀 Music Track Finder - Heroku Deployment"
echo "=========================================="
echo ""

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI is not installed"
    echo ""
    echo "Please install it from: https://devcenter.heroku.com/articles/heroku-cli"
    echo ""
    echo "Or run: brew tap heroku/brew && brew install heroku"
    exit 1
fi

echo "✅ Heroku CLI found"
echo ""

# Check if logged in
if ! heroku auth:whoami &> /dev/null; then
    echo "📝 Logging in to Heroku..."
    heroku login
else
    echo "✅ Already logged in to Heroku"
    heroku auth:whoami
fi

echo ""
echo "📋 Step 1: Create Heroku app"
echo ""

# Ask for app name
read -p "Enter app name (leave empty for random name): " APP_NAME

if [ -z "$APP_NAME" ]; then
    echo "Creating app with random name..."
    heroku create
else
    echo "Creating app: $APP_NAME..."
    heroku create $APP_NAME
fi

# Get the app name
APP_NAME=$(heroku apps:info --json | python3 -c "import sys, json; print(json.load(sys.stdin)['app']['name'])")

echo ""
echo "✅ App created: $APP_NAME"
echo ""

# Check if .env exists and get YouTube API key
if [ -f ".env" ]; then
    YOUTUBE_API_KEY=$(grep YOUTUBE_API_KEY .env | cut -d '=' -f2)
else
    echo "⚠️  .env file not found"
fi

echo "📋 Step 2: Set environment variables"
echo ""

if [ -z "$YOUTUBE_API_KEY" ] || [ "$YOUTUBE_API_KEY" = "your_youtube_api_key_here" ]; then
    read -p "Enter your YouTube API key: " YOUTUBE_API_KEY
fi

heroku config:set YOUTUBE_API_KEY=$YOUTUBE_API_KEY --app $APP_NAME

echo ""
echo "✅ Environment variables configured"
echo ""

echo "📋 Step 3: Deploy to Heroku"
echo ""

# Initialize git if not already
if [ ! -d ".git" ]; then
    echo "Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit - Music Track Finder"
fi

# Add Heroku remote
heroku git:remote --app $APP_NAME

# Deploy
echo "Pushing to Heroku..."
git push heroku main 2>/dev/null || git push heroku master

if [ $? -eq 0 ]; then
    echo ""
    echo "============================================"
    echo "✅ Deployment successful!"
    echo "============================================"
    echo ""
    echo "🌐 Your app is live at:"
    heroku apps:info --app $APP_NAME | grep "Web URL" | awk '{print $3}'
    echo ""
    echo "📊 View logs:"
    echo "  heroku logs --tail --app $APP_NAME"
    echo ""
    echo "📱 Open app:"
    echo "  heroku open --app $APP_NAME"
    echo ""
    echo "💡 To update your app later:"
    echo "  git add ."
    echo "  git commit -m 'Update message'"
    echo "  git push heroku main"
    echo ""
else
    echo ""
    echo "❌ Deployment failed"
    echo "Check the error messages above"
    exit 1
fi
