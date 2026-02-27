#!/bin/bash

# Music Track Finder - Google Cloud Run Deployment Script

echo "🚀 Music Track Finder - Google Cloud Run Deployment"
echo "===================================================="
echo ""

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Google Cloud SDK (gcloud) is not installed"
    echo ""
    echo "Please install it from: https://cloud.google.com/sdk/docs/install"
    echo ""
    echo "Or run: brew install --cask google-cloud-sdk"
    exit 1
fi

echo "✅ Google Cloud SDK found"
echo ""

# Get project ID
echo "📋 Step 1: Select or enter your Google Cloud Project ID"
echo ""
echo "Your current project:"
gcloud config get-value project 2>/dev/null || echo "  (none set)"
echo ""
read -p "Enter your Google Cloud Project ID (or press Enter to use current): " PROJECT_ID

if [ -z "$PROJECT_ID" ]; then
    PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
fi

if [ -z "$PROJECT_ID" ]; then
    echo "❌ No project ID specified"
    exit 1
fi

echo ""
echo "Using project: $PROJECT_ID"
gcloud config set project $PROJECT_ID

echo ""
echo "📋 Step 2: Set up environment variables"
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found"
    echo "Creating .env from template..."
    cp .env.example .env
    echo ""
    echo "Please edit .env and add your API keys, then run this script again."
    exit 1
fi

# Read YouTube API key from .env
YOUTUBE_API_KEY=$(grep YOUTUBE_API_KEY .env | cut -d '=' -f2)

if [ -z "$YOUTUBE_API_KEY" ] || [ "$YOUTUBE_API_KEY" = "your_youtube_api_key_here" ]; then
    echo "⚠️  YouTube API key not configured in .env"
    read -p "Enter your YouTube API key: " YOUTUBE_API_KEY
fi

echo ""
echo "📋 Step 3: Enable required APIs"
echo ""
echo "Enabling Cloud Run API..."
gcloud services enable run.googleapis.com --project=$PROJECT_ID
echo "Enabling Container Registry API..."
gcloud services enable containerregistry.googleapis.com --project=$PROJECT_ID
echo "Enabling Cloud Build API..."
gcloud services enable cloudbuild.googleapis.com --project=$PROJECT_ID

echo ""
echo "📋 Step 4: Choose deployment region"
echo ""
echo "Recommended regions:"
echo "  1. us-central1 (Iowa) - Low latency for US"
echo "  2. us-east1 (South Carolina) - Low latency for US East"
echo "  3. europe-west1 (Belgium) - Low latency for Europe"
echo "  4. asia-northeast1 (Tokyo) - Low latency for Asia"
echo ""
read -p "Enter region (default: us-central1): " REGION
REGION=${REGION:-us-central1}

echo ""
echo "📋 Step 5: Set service name"
echo ""
read -p "Enter service name (default: music-track-finder): " SERVICE_NAME
SERVICE_NAME=${SERVICE_NAME:-music-track-finder}

echo ""
echo "📋 Step 6: Build and deploy"
echo ""
echo "Building Docker image..."
echo ""

# Deploy using Cloud Build and Cloud Run
gcloud run deploy $SERVICE_NAME \
    --source . \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --set-env-vars YOUTUBE_API_KEY=$YOUTUBE_API_KEY \
    --project=$PROJECT_ID

if [ $? -eq 0 ]; then
    echo ""
    echo "============================================"
    echo "✅ Deployment successful!"
    echo "============================================"
    echo ""
    echo "Your app is now running on Google Cloud Run!"
    echo ""
    echo "🌐 Service URL:"
    gcloud run services describe $SERVICE_NAME --region=$REGION --format='value(status.url)' --project=$PROJECT_ID
    echo ""
    echo "📊 View in Console:"
    echo "https://console.cloud.google.com/run/detail/$REGION/$SERVICE_NAME/metrics?project=$PROJECT_ID"
    echo ""
    echo "💡 Next steps:"
    echo "  1. Share the Service URL with your team"
    echo "  2. Bookmark the Console URL to monitor usage"
    echo "  3. Set up custom domain (optional)"
    echo ""
else
    echo ""
    echo "❌ Deployment failed"
    echo "Please check the error messages above"
    exit 1
fi
