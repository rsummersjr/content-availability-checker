from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class YouTubeClient:
    def __init__(self, api_key=None):
        self.api_key = api_key
        if self.api_key:
            self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        else:
            self.youtube = None

    def search(self, track_name, artist_name=''):
        """Search for a track on YouTube and YouTube Music"""
        if not self.youtube:
            return {
                'youtube_music': {
                    'available': False,
                    'error': 'YouTube API key not configured',
                    'setup_required': True
                },
                'youtube': {
                    'available': False,
                    'error': 'YouTube API key not configured',
                    'setup_required': True
                }
            }

        query = f"{track_name} {artist_name}".strip()

        try:
            # Search YouTube
            search_response = self.youtube.search().list(
                q=query,
                part='id,snippet',
                maxResults=5,
                type='video'
            ).execute()

            youtube_results = []
            youtube_music_results = []

            for item in search_response.get('items', []):
                video_data = {
                    'title': item['snippet']['title'],
                    'url': f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                    'channel': item['snippet']['channelTitle'],
                    'thumbnail': item['snippet']['thumbnails']['default']['url'],
                    'published_date': item['snippet'].get('publishedAt', '')
                }

                youtube_results.append(video_data)

                # YouTube Music links are the same, just different domain
                music_video_data = video_data.copy()
                music_video_data['url'] = f"https://music.youtube.com/watch?v={item['id']['videoId']}"
                youtube_music_results.append(music_video_data)

            return {
                'youtube_music': {
                    'available': len(youtube_music_results) > 0,
                    'results': youtube_music_results[:3],
                    'count': len(youtube_music_results)
                },
                'youtube': {
                    'available': len(youtube_results) > 0,
                    'results': youtube_results[:3],
                    'count': len(youtube_results)
                }
            }

        except HttpError as e:
            error_msg = f"YouTube API error: {str(e)}"
            return {
                'youtube_music': {'available': False, 'error': error_msg},
                'youtube': {'available': False, 'error': error_msg}
            }
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            return {
                'youtube_music': {'available': False, 'error': error_msg},
                'youtube': {'available': False, 'error': error_msg}
            }
