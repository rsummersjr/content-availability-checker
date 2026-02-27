# Music Track Finder

A web application that allows you to search for music tracks and check their availability across multiple streaming platforms.

## Supported Platforms

- ✅ **YouTube Music** (API integration available)
- ✅ **YouTube** (API integration available)
- ✅ **Deezer** (Free API, no authentication required)
- ⚙️ **Apple Music** (Requires Apple Developer account)
- ⚙️ **Amazon Music** (No public API - manual search link provided)
- ⚙️ **Tidal** (Requires authentication - manual search link provided)

## Features

### Single Search
- Search by track name only
- Search by track name AND artist name for more accurate results
- Real-time search across multiple platforms
- Display track details including artist, album, publication date, and direct links
- Shows the original publication/release date for each track on each platform

### Bulk Search
- Search multiple tracks at once
- Enter tracks in simple format: "Track Name, Artist Name" (one per line)
- Get a summary table showing availability across all platforms
- Yes/No indicators for each platform
- Click "View Details" to see full results for any track
- Perfect for comparing multiple songs or building playlists

### Content Monitoring (NEW!)
- **Automated tracking** - Monitor specific tracks for availability changes
- **Email notifications** - Get alerted when content becomes available or unavailable
- **Country-specific** - Track availability in different regions
- **Custom frequency** - Check every 1, 3, 6, 12, or 24 hours
- **Change history** - View historical availability data
- **Pause/Resume** - Control monitors without deleting them
- **Perfect for:**
  - Tracking new releases
  - Monitoring geo-restrictions
  - Detecting content removal
  - Research and analysis

### General
- Beautiful, responsive UI
- Handles API errors gracefully
- Mobile-friendly design
- Background job scheduler for automated monitoring

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone or navigate to the project directory:**
   ```bash
   cd music-track-finder
   ```

2. **Install required Python packages:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API keys (optional but recommended):**

   Copy the `.env.example` file to `.env`:
   ```bash
   cp .env.example .env
   ```

   Then edit the `.env` file and add your API keys:

   #### YouTube API Key (Recommended)
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Enable the YouTube Data API v3
   - Create credentials (API Key)
   - Copy the API key to your `.env` file

   #### Apple Music API Key (Optional)
   - Requires Apple Developer Program membership ($99/year)
   - Follow [Apple Music API documentation](https://developer.apple.com/documentation/applemusicapi)
   - Generate a developer token
   - Copy the token to your `.env` file

## Running the Application

1. **Start the Flask server:**
   ```bash
   python app.py
   ```

2. **Open your web browser and navigate to:**
   ```
   http://localhost:5000
   ```

3. **Start searching for tracks!**

## How to Use

1. Enter a track name (required)
2. Optionally enter an artist name for more accurate results
3. Click "Search"
4. View availability across all platforms
5. Click on links to open tracks in the respective platforms

## Platform API Status

### Fully Functional
- **Deezer**: Works out of the box, no API key required (includes release date)
- **YouTube/YouTube Music**: Works with free API key (recommended) (includes upload date)

### Requires Setup
- **Apple Music**: Requires paid Apple Developer account and API token (includes release date)
- **Amazon Music**: No public API available - provides manual search link
- **Tidal**: Requires OAuth authentication - provides manual search link

### Publication Date Information
- **YouTube/YouTube Music**: Shows video upload date to the platform
- **Deezer**: Shows album/track release date
- **Apple Music**: Shows official release date (when API is configured)
- **Amazon Music & Tidal**: Publication date not available (no API access)

## Project Structure

```
music-track-finder/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── .env.example               # Example environment variables
├── README.md                  # This file
├── api_clients/               # API client modules
│   ├── __init__.py
│   ├── youtube_client.py      # YouTube & YouTube Music
│   ├── deezer_client.py       # Deezer
│   ├── apple_music_client.py  # Apple Music
│   ├── amazon_music_client.py # Amazon Music (placeholder)
│   └── tidal_client.py        # Tidal (placeholder)
├── templates/
│   └── index.html             # Frontend HTML
└── static/
    ├── style.css              # Styling
    └── script.js              # Frontend JavaScript
```

## Troubleshooting

### YouTube API Issues
- **Error: "YouTube API key not configured"**
  - Add your YouTube API key to the `.env` file
  - Make sure the YouTube Data API v3 is enabled in Google Cloud Console

- **Error: "quotaExceeded"**
  - YouTube API has daily quota limits (10,000 units/day for free tier)
  - Wait 24 hours or upgrade your quota

### General Issues
- **Port 5000 already in use:**
  - Change the port in `app.py`: `app.run(debug=True, host='0.0.0.0', port=5001)`

- **Module not found errors:**
  - Make sure all dependencies are installed: `pip install -r requirements.txt`

## Future Enhancements

- Add Spotify integration
- Add SoundCloud integration
- Implement caching to reduce API calls
- Add favorite/bookmark functionality
- Export results to CSV/JSON
- Add audio preview players
- Implement rate limiting

## API Rate Limits

- **YouTube**: 10,000 units per day (free tier)
- **Deezer**: 50 requests per 5 seconds
- **Apple Music**: Varies based on developer account

## License

This project is for educational purposes. Please respect the terms of service of each streaming platform and their APIs.

## Contributing

Feel free to submit issues and enhancement requests!
