# Google Cloud Run Deployment Guide

## 🎯 Overview

Deploy your Music Track Finder to Google Cloud Run for 24/7 availability without keeping your computer on.

### Benefits:
- ✅ **No computer required** - Runs in the cloud 24/7
- ✅ **Cost-effective** - Free tier covers light usage (~2 million requests/month)
- ✅ **Auto-scaling** - Handles traffic spikes automatically
- ✅ **HTTPS included** - Secure by default
- ✅ **Easy updates** - Redeploy with one command

### Estimated Costs:
- **Free tier:** First 2 million requests/month, 360,000 GB-seconds/month
- **Expected cost:** **$0/month** for typical company usage (< 1000 searches/day)
- **If you exceed free tier:** ~$0.40 per 1 million requests

---

## 📋 Prerequisites

### 1. Google Cloud Account
You already have this! (You used it for YouTube API)

### 2. Install Google Cloud SDK

**On macOS:**
```bash
brew install --cask google-cloud-sdk
```

**Or download from:** https://cloud.google.com/sdk/docs/install

**Verify installation:**
```bash
gcloud --version
```

### 3. Authenticate
```bash
gcloud auth login
```
This will open your browser to sign in with your Google account.

---

## 🚀 Deployment Steps

### Option A: Automated Deployment (Recommended)

I've created a script that handles everything for you:

```bash
./deploy-to-cloudrun.sh
```

The script will:
1. ✅ Check if Google Cloud SDK is installed
2. ✅ Let you select your project
3. ✅ Configure environment variables
4. ✅ Enable required APIs
5. ✅ Build and deploy your app
6. ✅ Give you the public URL

**That's it!** The script handles all the complexity.

---

### Option B: Manual Deployment

If you prefer to do it manually:

#### Step 1: Set Your Project
```bash
# List your projects
gcloud projects list

# Set your project (use the same one as YouTube API)
gcloud config set project YOUR_PROJECT_ID
```

#### Step 2: Enable APIs
```bash
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

#### Step 3: Deploy
```bash
gcloud run deploy music-track-finder \
    --source . \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --set-env-vars YOUTUBE_API_KEY=YOUR_YOUTUBE_API_KEY
```

Replace `YOUR_YOUTUBE_API_KEY` with your actual API key.

#### Step 4: Get Your URL
After deployment completes, you'll see:
```
Service URL: https://music-track-finder-xxxxx-uc.a.run.app
```

**This is your public URL!** Share it with your team.

---

## 🔐 Security Configuration

### Environment Variables

Your API keys are stored as environment variables (not in code):

**To update environment variables:**
```bash
gcloud run services update music-track-finder \
    --region us-central1 \
    --set-env-vars YOUTUBE_API_KEY=new_key_here
```

### Access Control

**Current setup:** Public access (anyone with URL can use it)

**To restrict access to your company:**

#### Option 1: Require Authentication
```bash
gcloud run services update music-track-finder \
    --region us-central1 \
    --no-allow-unauthenticated
```
Then users must sign in with their Google accounts.

#### Option 2: Use Identity-Aware Proxy (IAP)
Set up IAP to restrict access to specific Google Workspace users.

#### Option 3: Add API Key/Password in App
Modify the app to require a password (I can help with this).

---

## 📊 Monitoring & Management

### View Your App in Console
```
https://console.cloud.google.com/run
```

### View Logs
```bash
# View recent logs
gcloud run logs read music-track-finder --region us-central1

# Tail logs in real-time
gcloud run logs tail music-track-finder --region us-central1
```

### View Metrics
Check requests, latency, and costs:
```
https://console.cloud.google.com/run/detail/us-central1/music-track-finder/metrics
```

### Check Quotas
Monitor your YouTube API usage:
```
https://console.cloud.google.com/apis/api/youtube.googleapis.com/quotas
```

---

## 🔄 Updating Your App

Made changes to the code? Redeploy:

```bash
./deploy-to-cloudrun.sh
```

Or manually:
```bash
gcloud run deploy music-track-finder \
    --source . \
    --region us-central1
```

Cloud Run will:
- Build the new version
- Deploy with zero downtime
- Automatically rollback if there are errors

---

## 🌐 Custom Domain (Optional)

Want to use `music.yourcompany.com` instead of the Cloud Run URL?

### Step 1: Verify Domain Ownership
```bash
gcloud domains verify yourcompany.com
```

### Step 2: Map Domain
```bash
gcloud run domain-mappings create \
    --service music-track-finder \
    --domain music.yourcompany.com \
    --region us-central1
```

### Step 3: Update DNS
Add the DNS records shown in the output to your domain provider.

---

## 💰 Cost Optimization

### Current Free Tier Limits:
- **Requests:** 2 million/month
- **CPU time:** 180,000 vCPU-seconds/month
- **Memory:** 360,000 GiB-seconds/month
- **Network:** 1 GB/month

### Typical Usage for Your App:
- **Per search:** ~0.5 seconds CPU, ~256 MB memory
- **1000 searches/day** = ~30,000 searches/month
- **Estimated cost:** **$0** (well within free tier)

### If You Exceed Free Tier:
- **Requests:** $0.40 per million
- **CPU:** $0.00002400 per vCPU-second
- **Memory:** $0.00000250 per GiB-second

**Example:** 10,000 searches/day = ~$5-10/month

### Cost Saving Tips:
1. Use minimum resources (Cloud Run auto-optimizes)
2. Set max instances to prevent runaway costs
3. Enable request timeout (default: 300s, set to 60s)

```bash
gcloud run services update music-track-finder \
    --region us-central1 \
    --max-instances 10 \
    --timeout 60
```

---

## 🆘 Troubleshooting

### Deployment Failed

**Error: "gcloud: command not found"**
```bash
# Install Google Cloud SDK
brew install --cask google-cloud-sdk
```

**Error: "Permission denied"**
```bash
# Re-authenticate
gcloud auth login
```

**Error: "API not enabled"**
```bash
# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

### App Not Working After Deployment

**Check logs:**
```bash
gcloud run logs read music-track-finder --region us-central1 --limit 50
```

**Check environment variables:**
```bash
gcloud run services describe music-track-finder --region us-central1
```

**Test the endpoint:**
```bash
curl https://your-service-url.run.app
```

### YouTube API Not Working

**Check environment variable is set:**
```bash
gcloud run services describe music-track-finder \
    --region us-central1 \
    --format='value(spec.template.spec.containers[0].env)'
```

**Update API key:**
```bash
gcloud run services update music-track-finder \
    --region us-central1 \
    --set-env-vars YOUTUBE_API_KEY=your_key_here
```

---

## 📝 Post-Deployment Checklist

- [ ] App deployed successfully
- [ ] Service URL is accessible
- [ ] YouTube search works (API key configured)
- [ ] Deezer search works
- [ ] All platforms show correct status
- [ ] Share URL with team
- [ ] Bookmark Cloud Console URL
- [ ] Set up monitoring/alerts (optional)
- [ ] Configure custom domain (optional)
- [ ] Set up access restrictions (optional)

---

## 🎉 Success!

Once deployed, your app will be:
- ✅ Available 24/7
- ✅ Accessible from anywhere via HTTPS
- ✅ Auto-scaling based on demand
- ✅ Backed up and managed by Google
- ✅ Free (or very cheap) to run

**Share this URL with your company:**
```
https://music-track-finder-xxxxx-uc.a.run.app
```

**No more keeping your computer on!** 🎊

---

## 📞 Support

**Google Cloud Run Documentation:**
https://cloud.google.com/run/docs

**Pricing Calculator:**
https://cloud.google.com/products/calculator

**Status Dashboard:**
https://status.cloud.google.com/

Need help? Just ask!
