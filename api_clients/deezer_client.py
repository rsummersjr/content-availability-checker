import requests

class DeezerClient:
    def __init__(self):
        self.base_url = 'https://api.deezer.com'

    def search(self, track_name, artist_name=''):
        """Search for a track on Deezer"""
        query = f"{track_name} {artist_name}".strip()

        try:
            response = requests.get(
                f"{self.base_url}/search",
                params={'q': query, 'limit': 5},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()

            results = []
            for track in data.get('data', []):
                # Get release date from album if available
                release_date = track.get('album', {}).get('release_date', '')

                results.append({
                    'title': track['title'],
                    'artist': track['artist']['name'],
                    'album': track['album']['title'],
                    'url': track['link'],
                    'preview': track.get('preview'),
                    'thumbnail': track['album'].get('cover_small'),
                    'published_date': release_date
                })

            return {
                'available': len(results) > 0,
                'results': results[:3],
                'count': len(results)
            }

        except requests.exceptions.RequestException as e:
            return {
                'available': False,
                'error': f"Deezer API error: {str(e)}"
            }
        except Exception as e:
            return {
                'available': False,
                'error': f"Error: {str(e)}"
            }
