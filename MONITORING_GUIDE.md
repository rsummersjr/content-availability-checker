

# Content Monitoring Guide

Automatically track music availability changes across streaming platforms with email notifications.

## 🎯 What is Content Monitoring?

The monitoring feature allows you to:
- **Track specific tracks** for availability changes
- **Get automated email alerts** when content becomes available or unavailable
- **Monitor by country** to track region-specific availability
- **Set custom check frequencies** (hourly, every 6 hours, daily, etc.)
- **View change history** to see how availability has changed over time

---

## 🚀 Quick Start

### Step 1: Access Monitors

Click **"🔔 Manage Monitors"** from the main search page.

### Step 2: Create a Monitor

1. **Enter track details:**
   - Track Name (required)
   - Artist Name (optional but recommended)

2. **Configure monitoring:**
   - **Check Frequency**: How often to check (1, 3, 6, 12, or 24 hours)
   - **Country**: Which country/region to monitor from

3. **Set up notifications (optional):**
   - Toggle "Enable email notifications"
   - Enter your email address

4. Click **"Create Monitor"**

### Step 3: Monitor is Active!

Your track will now be:
- ✅ Checked automatically at your chosen frequency
- ✅ Monitored for availability changes
- ✅ Ready to send email alerts (if configured)

---

## 📧 Email Notifications

### What You'll Receive

When content availability changes, you'll get an email with:

**Subject:** `Content Availability Change Alert: [Track Name]`

**Content:**
- Track and artist name
- Which platform(s) changed
- Type of change (now available / no longer available)
- Timestamp of detection
- Link to view full details (coming soon)

### Example Email:

```
🎵 Content Availability Alert

Track: Bohemian Rhapsody
Artist: Queen
Checked: 2026-02-27 14:30 UTC

Changes Detected:

YouTube Music: ✅ Content is now available
Deezer: ❌ Content is no longer available

This is an automated notification from Music Track Finder.
```

### Setting Up Email (Optional)

**For Development/Testing:**
- Leave SMTP settings blank in `.env`
- Emails will be logged to console (simulation mode)

**For Production:**
1. Edit `.env` file and add:
   ```
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USERNAME=your_email@gmail.com
   SMTP_PASSWORD=your_app_password
   SMTP_FROM_EMAIL=noreply@musictrackfinder.com
   ```

2. For Gmail:
   - Use an [App Password](https://support.google.com/accounts/answer/185833)
   - Enable 2-factor authentication first
   - Generate app-specific password

---

## 🌍 Country-Specific Monitoring

### Why Monitor by Country?

Music availability varies by region due to:
- Licensing agreements
- Geographic restrictions
- Regional release schedules

### Supported Countries:

- 🇺🇸 **United States** (US)
- 🇬🇧 **United Kingdom** (GB)
- 🇨🇦 **Canada** (CA)
- 🇦🇺 **Australia** (AU)
- 🇩🇪 **Germany** (DE)
- 🇫🇷 **France** (FR)
- 🇯🇵 **Japan** (JP)
- 🇧🇷 **Brazil** (BR)
- 🇮🇳 **India** (IN)
- 🇲🇽 **Mexico** (MX)

### How It Works:

When you select a country:
- API requests are made as if from that region
- Results reflect availability in that country
- Changes are detected for that specific region

---

## ⏱️ Check Frequencies

### Available Options:

| Frequency | Best For |
|-----------|----------|
| **Every hour** | New releases, time-sensitive content |
| **Every 3 hours** | Recently released tracks |
| **Every 6 hours** | General monitoring (recommended) |
| **Every 12 hours** | Stable content, occasional checks |
| **Every 24 hours** | Archive content, low-priority monitors |

### Recommendations:

- **New Releases:** 1-3 hours for first week, then increase
- **General Tracking:** 6-12 hours is usually sufficient
- **Archive Content:** 24 hours to conserve API quota

---

## 📊 Managing Monitors

### Monitor Card Actions

Each monitor has four actions:

**1. Check Now**
- Performs an immediate check
- Updates availability status
- Sends notification if changes detected
- Doesn't affect scheduled check time

**2. Pause/Resume**
- **Pause**: Stops automatic checks (monitor stays in database)
- **Resume**: Reactivates automatic checking
- Useful for temporarily disabling without deleting

**3. View History**
- Shows last 20 checks
- Displays changes detected
- Shows notification status
- Helps track availability patterns

**4. Delete**
- Permanently removes monitor
- Deletes all check history
- Cannot be undone
- Stops all notifications

### Monitor Status

**Active** (Green Badge)
- Currently being monitored
- Automatic checks running
- Notifications enabled (if configured)

**Inactive** (Red Badge)
- Paused by user
- No automatic checks
- No notifications sent

---

## 🔍 Understanding Availability States

### Platform Status Indicators:

**✓ Available** (Green)
- Track found on platform
- Can be played/purchased
- Direct links available

**✗ Unavailable** (Red)
- Track not found
- May be removed or geo-blocked
- No access in monitored region

### Common Scenarios:

**Content Removed:**
- License expired
- Artist/label removed it
- Platform removed it

**Content Added:**
- New release went live
- Geo-restrictions lifted
- Platform acquired license

**Availability Changed:**
- Was available → Now unavailable
- Was unavailable → Now available

---

## 💡 Use Cases

### 1. Track New Releases

**Scenario:** Waiting for a new album to drop

```
Track: New Album Title
Artist: Artist Name
Frequency: Every hour
Notifications: Yes
```

**Benefit:** Get notified the moment it's available

### 2. Monitor Geo-Restrictions

**Scenario:** Track available in US but not your country

```
Track: Song Name
Country: Your Country
Frequency: Every 12 hours
Notifications: Yes
```

**Benefit:** Know when it becomes available in your region

### 3. Track Content Removal

**Scenario:** Ensure your favorite tracks don't disappear

```
Track: Favorite Song
Frequency: Every 24 hours
Notifications: Yes
```

**Benefit:** Get alerted if content is removed

### 4. Research Availability Patterns

**Scenario:** Understanding platform licensing

```
Multiple monitors for same track, different platforms
Frequency: Every 6 hours
Notifications: No (check history manually)
```

**Benefit:** See which platforms have content first

---

## 🛠️ Technical Details

### How Monitoring Works:

1. **Background Scheduler:**
   - Runs every hour
   - Checks for due monitors
   - Processes them automatically

2. **Change Detection:**
   - Compares current state with last known state
   - Detects availability changes per platform
   - Stores change history

3. **Notification System:**
   - Triggered only when changes detected
   - Sends formatted email
   - Logs notification status

### API Quota Considerations:

**YouTube API:**
- Free tier: 10,000 units/day
- Per search: ~100 units
- Max monitors per day: ~100 (at 1-hour frequency)

**Recommendations:**
- Use longer frequencies (6-24 hours) for most monitors
- Reserve hourly checks for critical monitors
- Monitor quota at [Google Cloud Console](https://console.cloud.google.com/apis/dashboard)

---

## 🔐 Privacy & Security

### Data Storage:

**Stored in Database:**
- Track name and artist
- Email address (encrypted in production)
- Check history
- Availability states

**NOT Stored:**
- SMTP passwords (environment variables only)
- Full search results (only availability state)
- Personal information beyond email

### Email Security:

- Use app-specific passwords (not main password)
- SMTP connections use TLS/STARTTLS
- Emails sent only when changes detected
- Unsubscribe by deleting monitor

---

## 🆘 Troubleshooting

### "Monitor not checking"

**Check:**
- Monitor status is "Active"
- Next check time hasn't passed yet
- Server is running
- No errors in logs

**Solution:**
- Click "Check Now" to test
- Verify monitor is active
- Check server logs

### "No email received"

**Check:**
- Email notifications enabled
- Email address correct
- Changes were actually detected
- SMTP settings configured

**Solution:**
- Check spam folder
- Verify SMTP settings in `.env`
- Look for "Email sent" in logs
- Try "Check Now" to trigger manually

### "Check failed"

**Possible Causes:**
- API quota exceeded (YouTube)
- Network issues
- Invalid track name
- Platform API down

**Solution:**
- Check API quotas
- Verify track name spelling
- Try manual search first
- Check platform status

### "Emails going to spam"

**Solutions:**
- Add sender to contacts
- Configure SPF/DKIM records (advanced)
- Use reputable SMTP service
- Whitelist sender domain

---

## 📈 Best Practices

### Monitor Setup:

1. **Start with few monitors** - Test before scaling up
2. **Use longer frequencies** - Conserve API quota
3. **Be specific** - Include artist names for accuracy
4. **Test first** - Do manual search before creating monitor

### Email Notifications:

1. **Use email for important tracks only** - Avoid alert fatigue
2. **Group by priority** - Critical tracks = short frequency + email
3. **Review periodically** - Delete unused monitors
4. **Check spam regularly** - Don't miss important alerts

### Performance:

1. **Limit active monitors** - Keep under 50 for free tier
2. **Adjust frequencies** - Longer = less API usage
3. **Pause unused monitors** - Don't delete if you might need later
4. **Archive history** - Delete very old monitors

---

## 🎓 Advanced Features (Coming Soon)

- Custom notification templates
- Webhook integrations
- Slack/Discord notifications
- Multi-region monitoring per track
- Availability analytics dashboard
- Export history to CSV
- Monitor groups/playlists

---

## 📞 Support

**Need Help?**
- Check this guide
- Review server logs
- Test with manual search first
- Create GitHub issue

**Feature Requests:**
- Submit via GitHub Issues
- Include use case
- Describe desired behavior

---

**Happy Monitoring! 🎵**

Track your favorite music and never miss when it becomes available!
