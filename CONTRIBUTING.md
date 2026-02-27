# Contributing to Music Track Finder

Thank you for contributing to the Music Track Finder! This guide will help you get started.

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Git installed
- GitHub account

### Setup for Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/rsummersjr/content-availability-checker.git
   cd content-availability-checker
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   ```

   Then edit `.env` and add your API keys:
   - `YOUTUBE_API_KEY` - Get from Google Cloud Console
   - `APPLE_MUSIC_API_KEY` - (Optional) Get from Apple Developer

5. **Run the application:**
   ```bash
   python3 app.py
   ```

   The app will be available at: http://localhost:5001

---

## 🔑 Getting API Keys

### YouTube Data API v3 Key (Free)
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable "YouTube Data API v3"
4. Create credentials → API Key
5. Copy the key to your `.env` file

### Apple Music API Key (Optional - $99/year)
1. Requires Apple Developer Program membership
2. See [Apple Music API Documentation](https://developer.apple.com/documentation/applemusicapi)

---

## 📁 Project Structure

```
content-availability-checker/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── api_clients/               # API integration modules
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

---

## 🔄 Development Workflow

### 1. Create a Branch
```bash
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes
- Write clean, readable code
- Follow existing code style
- Test your changes locally

### 3. Commit Your Changes
```bash
git add .
git commit -m "Description of your changes"
```

Good commit message examples:
- `Add Spotify API integration`
- `Fix YouTube search bug for special characters`
- `Update UI to show album artwork`

### 4. Push to GitHub
```bash
git push origin feature/your-feature-name
```

### 5. Create a Pull Request
1. Go to the repository on GitHub
2. Click "Pull requests" → "New pull request"
3. Select your branch
4. Add a description of your changes
5. Click "Create pull request"

---

## 🧪 Testing

### Manual Testing
1. Start the app locally
2. Test search functionality:
   - Search by track name only
   - Search by track name + artist
   - Verify all platforms show correct status
   - Check publication dates are displayed

### Test Different Scenarios
- Popular tracks (e.g., "Bohemian Rhapsody" by "Queen")
- Obscure tracks
- Tracks with special characters
- Empty searches (should show error)

---

## 🎨 Code Style Guidelines

### Python
- Use 4 spaces for indentation (not tabs)
- Follow PEP 8 style guide
- Add docstrings to functions
- Keep functions focused and small

### JavaScript
- Use 2 spaces for indentation
- Use meaningful variable names
- Add comments for complex logic

### CSS
- Follow existing naming conventions
- Keep selectors specific but not overly complex

---

## 📝 Adding New Features

### Adding a New Music Platform

1. **Create a new client file:**
   ```python
   # api_clients/spotify_client.py
   class SpotifyClient:
       def __init__(self, api_key=None):
           self.api_key = api_key

       def search(self, track_name, artist_name=''):
           # Implement search logic
           return {
               'available': True/False,
               'results': [...],
               'count': 0
           }
   ```

2. **Update app.py:**
   ```python
   from api_clients.spotify_client import SpotifyClient

   spotify_client = SpotifyClient(api_key=os.getenv('SPOTIFY_API_KEY'))

   # In search route:
   results['platforms']['spotify'] = spotify_client.search(track_name, artist_name)
   ```

3. **Update frontend (index.html):**
   ```html
   <div class="platform-card" id="spotify-card">
       <div class="platform-header">
           <h3>Spotify</h3>
           <span class="status-badge"></span>
       </div>
       <div class="platform-content"></div>
   </div>
   ```

4. **Update frontend (script.js):**
   ```javascript
   displayPlatform('spotify', data.platforms.spotify);
   ```

---

## 🐛 Reporting Issues

Found a bug? Please create an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Screenshots (if applicable)
- Your environment (OS, Python version, browser)

---

## 💡 Feature Requests

Have an idea? Create an issue with:
- Clear description of the feature
- Use case / why it's needed
- Proposed implementation (if you have ideas)

---

## 🔐 Security

### Important Rules:
- **NEVER commit API keys** to the repository
- Always use `.env` file for sensitive data
- The `.env` file is in `.gitignore` - keep it that way!
- If you accidentally commit a key, revoke it immediately

### If You Find a Security Issue:
- DO NOT create a public issue
- Contact the repository owner directly
- Describe the vulnerability
- Provide steps to reproduce

---

## 📦 Deployment

### Deploy Your Own Instance

**Render (Free):**
1. Fork the repository
2. Sign up at https://render.com
3. Connect your GitHub account
4. Create new Web Service from your fork
5. Add environment variables
6. Deploy!

**Heroku:**
1. Install Heroku CLI: `brew install heroku`
2. Run: `heroku login`
3. Run: `./deploy-to-heroku.sh`

**Google Cloud Run:**
- See `GOOGLE_CLOUD_RUN_DEPLOYMENT.md`

---

## 📞 Getting Help

- Check existing issues and pull requests
- Read the README.md
- Review the documentation files
- Ask questions in pull request comments

---

## 🎉 Thank You!

Your contributions make this project better for everyone. Happy coding! 🎵

---

## 📄 License

This project is for educational and internal use. Please respect the terms of service of each music platform's API.
