# Team Setup Guide

Quick guide for team members to get started with the Music Track Finder.

## 🎯 For Team Members

### Quick Start (5 minutes)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/rsummersjr/content-availability-checker.git
   cd content-availability-checker
   ```

2. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Set up environment:**
   ```bash
   cp .env.example .env
   ```

4. **Get API keys** (ask team lead):
   - YouTube API key (required for YouTube/YouTube Music)
   - Add to `.env` file

5. **Run the app:**
   ```bash
   python3 app.py
   ```

6. **Open in browser:**
   ```
   http://localhost:5001
   ```

---

## 🔑 API Keys Needed

### Required for Full Functionality:
- **YouTube Data API v3 Key** - For YouTube/YouTube Music searches

### Optional:
- **Apple Music API Key** - For Apple Music searches (requires $99/year Apple Developer account)

### No Key Required:
- **Deezer** - Works out of the box!
- **Amazon Music & Tidal** - Manual search links provided

---

## 📧 Contact Team Lead For:
- YouTube API key
- Apple Music API key (if available)
- Deployment access
- Repository permissions

---

## 🛠️ Development

See `CONTRIBUTING.md` for full development guidelines.

**Quick commands:**
```bash
# Run locally
python3 app.py

# Check status (if deployed)
./check-status.sh

# Stop local server
Ctrl+C
```

---

## 🌐 Deployed App

**Production URL:** [To be added after deployment]

**Staging URL:** [To be added if needed]

---

## 📚 Documentation

- `README.md` - Overview and features
- `CONTRIBUTING.md` - Development guidelines
- `DEPLOYMENT_GUIDE.md` - Deployment options
- `COMPANY_ACCESS.md` - End-user instructions

---

## 🆘 Troubleshooting

**Can't install dependencies?**
```bash
python3 -m pip install --upgrade pip
pip3 install -r requirements.txt
```

**Port 5001 already in use?**
Edit `app.py` and change port to 5002 or another available port.

**YouTube searches not working?**
- Check `.env` file has `YOUTUBE_API_KEY=your_key_here`
- Verify API key is correct
- Check API quota in Google Cloud Console

**Questions?**
Contact the repository owner or create an issue on GitHub.
