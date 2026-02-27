# Changelog

## Version 1.1.0 - Publication Date Feature

### Added
- **Publication/Release Date Display**: Each track now shows when it was first published to the platform
  - YouTube/YouTube Music: Shows video upload date
  - Deezer: Shows album/track release date
  - Apple Music: Shows official release date
  - Date is displayed in a user-friendly format (e.g., "January 15, 2024")
  - Date appears with a calendar icon (📅) for easy identification

### Modified
- Updated `youtube_client.py` to fetch and return `publishedAt` date
- Updated `deezer_client.py` to fetch and return album `release_date`
- Updated `apple_music_client.py` to fetch and return track `releaseDate`
- Enhanced frontend JavaScript with date formatting function
- Added CSS styling for publication date display
- Updated README with publication date information

### Technical Details
- Date format: ISO 8601 from APIs, displayed as "Month DD, YYYY"
- Graceful handling of missing dates (doesn't display if unavailable)
- Dates are validated before display to prevent errors

---

## Version 1.0.0 - Initial Release

### Features
- Multi-platform music track search
- Support for 6 streaming platforms
- YouTube and Deezer API integration
- Responsive web interface
- Track metadata display (title, artist, album)
- Direct links to platform pages
- Error handling and API status indicators
