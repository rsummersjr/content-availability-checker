# Quick Start: Deploy to Google Cloud Run

## ✅ What's Ready

I've already set up everything you need:
- ✅ Dockerfile (containerizes your app)
- ✅ Deployment script (automated deployment)
- ✅ Environment configuration
- ✅ Google Cloud SDK is installed on your machine

## 🚀 Deploy in 3 Steps (5-10 minutes)

### Step 1: Authenticate with Google Cloud

```bash
gcloud auth login
```

This will:
- Open your browser
- Ask you to sign in with your Google account (same one you used for YouTube API)
- Grant permissions

### Step 2: Run the Deployment Script

```bash
cd music-track-finder
./deploy-to-cloudrun.sh
```

The script will ask you:
1. **Project ID** - Use the same project where you have YouTube API enabled
2. **Region** - Press Enter for default (us-central1)
3. **Service name** - Press Enter for default (music-track-finder)

Then it will:
- Enable required APIs
- Build your app
- Deploy to Cloud Run
- Give you a public URL

### Step 3: Share with Your Team

The script will output something like:
```
🌐 Service URL: https://music-track-finder-xxxxx-uc.a.run.app
```

**That's your public URL!** Share it with your company.

---

## 📋 What to Expect

### During Deployment (~5-10 minutes):
```
Building Docker image...        [2-3 min]
Uploading to Cloud Run...       [1-2 min]
Deploying service...            [2-3 min]
Verifying deployment...         [30 sec]
```

### After Deployment:
- ✅ App is live at a public HTTPS URL
- ✅ Available 24/7 (no computer needed)
- ✅ Auto-scales with usage
- ✅ Likely $0/month (within free tier)

---

## 🎯 Pro Tips

### Before You Deploy:
- ✅ Make sure your YouTube API key is in `.env` file
- ✅ Close/stop your local server (not required, but cleaner)
- ✅ Be ready to wait 5-10 minutes

### After You Deploy:
- 📱 Test the URL yourself first
- 📧 Share URL with your team
- 📊 Bookmark the Cloud Console to monitor usage
- 💾 Keep the deployment script for future updates

### To Update Later:
Just run the deployment script again:
```bash
./deploy-to-cloudrun.sh
```

---

## ⚡ Ready to Deploy?

Run these commands now:

```bash
# Step 1: Authenticate
gcloud auth login

# Step 2: Deploy
./deploy-to-cloudrun.sh
```

**That's it!** You'll have a public URL in ~10 minutes.

---

## ❓ Need Help?

### "Which project ID should I use?"

Find your project ID:
```bash
gcloud auth login
gcloud projects list
```

Use the project where you enabled YouTube Data API v3.

### "What region should I choose?"

- **us-central1** - Good for most US companies
- **us-east1** - Good for East Coast US
- **europe-west1** - Good for Europe
- **asia-northeast1** - Good for Asia

Default (us-central1) works great for most cases.

### "How much will this cost?"

Free tier includes:
- 2 million requests/month
- 180,000 vCPU-seconds/month
- 360,000 GiB-seconds/month

Your app will likely cost **$0/month** unless you get massive traffic.

---

## 🎉 What You Get

After deployment:
- 🌐 Public HTTPS URL
- 🔒 Secure by default
- 📈 Auto-scaling
- 💰 Free (or very cheap)
- 🚀 No computer needed
- ⚡ Fast global access

**Your team can access it from anywhere, anytime!**
