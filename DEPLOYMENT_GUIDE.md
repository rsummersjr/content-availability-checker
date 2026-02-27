# Company Deployment Guide - Local Network

## 📍 Current Status

Your Music Track Finder is running and accessible to anyone on your company network!

### Access URLs (Share with colleagues):
- **Primary:** `http://192.168.86.25:5001`
- **Alternative:** `http://172.21.6.180:5001`
- **Local (you only):** `http://127.0.0.1:5001`

---

## 🎯 Quick Server Management

### Check if Server is Running
```bash
./check-status.sh
```

### Start the Server
```bash
./start-server.sh
```

### Stop the Server
```bash
./stop-server.sh
```

---

## 📧 Sharing with Your Team

1. **Send them the access document:**
   - Share `COMPANY_ACCESS.md` via email or Slack
   - Or just send them the URL: `http://192.168.86.25:5001`

2. **They can access immediately** if on the same network

3. **Requirements for users:**
   - Must be on company network (same WiFi/VPN)
   - Any modern web browser
   - No installation needed!

---

## ⚙️ Server Management Tips

### Keeping the Server Running

**Option A: Keep Terminal Open**
- Run `./start-server.sh`
- Keep the terminal window open
- Don't close your laptop lid (or disable sleep)

**Option B: Run in Background (Advanced)**
```bash
# Start in background
nohup python3 app.py > server.log 2>&1 &

# Check if running
./check-status.sh

# Stop background server
./stop-server.sh
```

**Option C: Auto-start on Login (macOS)**
Create a LaunchAgent to start automatically when you log in.
(Let me know if you need help setting this up!)

### Important Notes:

⚠️ **Server will stop when:**
- You close the terminal (unless using background mode)
- Your computer restarts
- Your computer goes to sleep
- You log out

✅ **Server will continue when:**
- You minimize the terminal
- You switch to other applications
- You're using the computer normally

---

## 🔒 Security Considerations

### Current Setup:
- ✅ Running on internal network only
- ✅ API keys stored in `.env` (not shared with users)
- ✅ Read-only access (users can only search, not modify)

### Best Practices:
- Don't share your `.env` file
- Don't commit `.env` to git (already in `.gitignore`)
- Only share access with trusted company members
- Consider firewall rules if needed

---

## 📊 Usage Monitoring

### View Server Logs
```bash
# If running in foreground, watch the terminal output
# If running in background:
tail -f server.log
```

### API Quota (YouTube)
- Free tier: 10,000 units/day
- Each search uses ~100 units
- Can handle ~100 searches per day
- Monitor at: https://console.cloud.google.com/apis/dashboard

---

## 🚀 Future Upgrade Paths

When you need more reliability or accessibility:

### 1. **Dedicated Server**
   - Run on an always-on company server
   - No dependency on your laptop

### 2. **Cloud Deployment**
   - Deploy to Heroku, AWS, or Google Cloud
   - Accessible from anywhere
   - Always available

### 3. **Docker Container**
   - Package everything in a container
   - Easy deployment anywhere
   - Consistent environment

**Need help with upgrades? Just ask!**

---

## 🆘 Troubleshooting

### Users Can't Access the App

**Check 1: Is the server running?**
```bash
./check-status.sh
```

**Check 2: Are they on the same network?**
- They must be on company WiFi/VPN
- Test from your computer first: `http://192.168.86.25:5001`

**Check 3: Firewall blocking?**
- Check macOS firewall settings
- System Preferences → Security & Privacy → Firewall

**Check 4: IP address changed?**
- Your IP might change if you reconnect to network
- Run: `ifconfig | grep "inet "` to get current IP
- Update the URLs you shared

### Server Won't Start

**Port already in use:**
```bash
./stop-server.sh
./start-server.sh
```

**Dependencies missing:**
```bash
pip3 install -r requirements.txt
```

---

## 📞 Support

**For server issues:**
- Check server logs
- Run `./check-status.sh`
- Restart with `./stop-server.sh` then `./start-server.sh`

**For user issues:**
- Verify they're using correct URL
- Confirm they're on company network
- Test the URL yourself first

---

## ✅ Quick Checklist for Sharing

- [ ] Server is running (`./check-status.sh`)
- [ ] You can access it locally (http://127.0.0.1:5001)
- [ ] Share URL with colleagues (http://192.168.86.25:5001)
- [ ] Share `COMPANY_ACCESS.md` instructions
- [ ] Keep terminal open or run in background
- [ ] Monitor API quota if needed

**All set! Your team can now search for music tracks across multiple platforms! 🎵**
