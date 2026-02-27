# Bulk Search Guide

Learn how to use the bulk search feature to search for multiple tracks at once.

## 🎯 What is Bulk Search?

Bulk search allows you to search for multiple music tracks simultaneously and get a summary table showing their availability across all platforms.

## 📝 How to Use

### Step 1: Switch to Bulk Search Mode

1. Open the Music Track Finder app
2. Click the **"Bulk Search"** button at the top of the search section

### Step 2: Enter Your Tracks

In the text area, enter your tracks using this format:

```
Track Name, Artist Name
```

**One track per line.** For example:

```
Bohemian Rhapsody, Queen
Billie Jean, Michael Jackson
Imagine, John Lennon
Hotel California, Eagles
Shape of You, Ed Sheeran
```

**Notes:**
- Artist name is optional (you can just enter track names)
- Commas separate track from artist
- One track per line
- Empty lines are ignored

### Step 3: Search

Click the **"Search All"** button.

The app will:
- Search for each track across all platforms
- Show a progress indicator
- Display a summary table when complete

### Step 4: View Results

You'll see a table with:

| Column | Description |
|--------|-------------|
| **Track** | The track name |
| **Artist** | The artist name (or "Not specified") |
| **Platform Columns** | "Yes", "No", or "Setup" for each platform |
| **Details** | Link to view full search results |

**Platform Availability:**
- ✅ **Yes** (Green) - Track found on this platform
- ❌ **No** (Red) - Track not found
- ⚙️ **Setup** (Orange) - Platform requires API configuration

### Step 5: View Details

Click **"View Details"** for any track to see:
- Full search results for that track
- Direct links to the track on each platform
- Publication dates
- Album information
- Artist details

---

## 💡 Use Cases

### 1. Playlist Comparison

Check if your entire playlist is available across platforms:

```
Blinding Lights, The Weeknd
Levitating, Dua Lipa
Save Your Tears, The Weeknd
Good 4 U, Olivia Rodrigo
Peaches, Justin Bieber
```

### 2. Album Availability Check

Check if all tracks from an album are available:

```
Bohemian Rhapsody, Queen
Love of My Life, Queen
You're My Best Friend, Queen
'39, Queen
```

### 3. Artist Discography Research

Check availability of an artist's popular songs:

```
Like a Rolling Stone, Bob Dylan
Blowin' in the Wind, Bob Dylan
The Times They Are a-Changin', Bob Dylan
Mr. Tambourine Man, Bob Dylan
```

### 4. Music Discovery

Compare availability of similar songs or covers:

```
Hallelujah, Leonard Cohen
Hallelujah, Jeff Buckley
Hallelujah, Rufus Wainwright
```

---

## 📊 Understanding the Results

### Summary Table

The table gives you a quick overview:
- **Rows**: Each track you searched for
- **Columns**: Each streaming platform
- **Cells**: Availability status (Yes/No/Setup)

### Detailed View

Click "View Details" to see:
- **YouTube Music**: Video titles, channels, upload dates
- **YouTube**: Same as YouTube Music
- **Deezer**: Track titles, artists, albums, release dates
- **Apple Music**: (If configured) Track details and release dates
- **Amazon Music**: Manual search link
- **Tidal**: Manual search link

---

## ⚡ Tips & Tricks

### Format Tips

**Good formats:**
```
Track Name, Artist Name
Track Name
"Track Name with Comma", Artist Name
```

**What works:**
- Simple track names
- Track and artist
- Just track names (no artist)

**What doesn't work:**
- Multiple tracks on one line
- Invalid characters
- Empty lines (they're skipped)

### Best Practices

1. **Start small** - Test with 3-5 tracks first
2. **Be specific** - Include artist names for better accuracy
3. **Check spelling** - Typos will return "No" results
4. **Use official names** - Match the official track/artist names

### Performance

- **Small batches** (1-10 tracks): ~5-10 seconds
- **Medium batches** (10-50 tracks): ~30-60 seconds
- **Large batches** (50+ tracks): 1-2 minutes

**Note:** YouTube API has daily quota limits. Very large batches may hit quota limits.

---

## 🔄 Switching Back to Single Search

Click the **"Single Search"** button to return to regular one-at-a-time searching.

---

## 🆘 Troubleshooting

### "No valid tracks found"
- Check your format: `Track Name, Artist Name`
- Make sure you have at least one track entered
- Remove any extra commas or special characters

### Results show all "No"
- Check track/artist spelling
- Try searching without artist name
- Try the single search mode to verify the track exists

### Slow performance
- Large batches take longer
- YouTube API may have rate limits
- Try smaller batches (10-20 tracks max)

### "Setup" for all results
- Some platforms require API keys
- See README.md for API setup instructions
- YouTube and Deezer work without special setup

---

## 📧 Example Bulk Searches

### Classic Rock Hits
```
Stairway to Heaven, Led Zeppelin
Hotel California, Eagles
Bohemian Rhapsody, Queen
Sweet Child O' Mine, Guns N' Roses
November Rain, Guns N' Roses
```

### Modern Pop
```
Blinding Lights, The Weeknd
Levitating, Dua Lipa
drivers license, Olivia Rodrigo
Good 4 U, Olivia Rodrigo
Positions, Ariana Grande
```

### 90s Hip Hop
```
Juicy, The Notorious B.I.G.
California Love, 2Pac
Gin and Juice, Snoop Dogg
Hypnotize, The Notorious B.I.G.
It Was a Good Day, Ice Cube
```

---

## 🎉 Advanced Features

### Export Results (Future Feature)
- Coming soon: Export to CSV
- Coming soon: Share results URL
- Coming soon: Save searches

### Filters (Future Feature)
- Filter by platform
- Show only available tracks
- Sort by availability count

---

**Happy Bulk Searching! 🎵**
