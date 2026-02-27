import requests

class AppleMusicClient:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.base_url = 'https://api.music.apple.com/v1'

    def search(self, track_name, artist_name=''):
        """Search for a track on Apple Music"""
        if not self.api_key:
            return {
                'available': False,
                'error': 'Apple Music API key not configured',
                'setup_required': True,
                'note': 'Requires Apple Developer account and Music API token'
            }

        query = f"{track_name} {artist_name}".strip()

        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}'
            }

            response = requests.get(
                f"{self.base_url}/catalog/us/search",
                headers=headers,
                params={'term': query, 'types': 'songs', 'limit': 5},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()

            results = []
            songs = data.get('results', {}).get('songs', {}).get('data', [])

            for song in songs:
                attributes = song['attributes']
                results.append({
                    'title': attributes['name'],
                    'artist': attributes['artistName'],
                    'album': attributes['albumName'],
                    'url': attributes.get('url'),
                    'preview': attributes.get('previews', [{}])[0].get('url'),
                    'thumbnail': attributes.get('artwork', {}).get('url', '').replace('{w}', '100').replace('{h}', '100'),
                    'published_date': attributes.get('releaseDate', '')
                })

            return {
                'available': len(results) > 0,
                'results': results,
                'count': len(results)
            }

        except requests.exceptions.RequestException as e:
            return {
                'available': False,
                'error': f"Apple Music API error: {str(e)}"
            }
        except Exception as e:
            return {
                'available': False,
                'error': f"Error: {str(e)}"
            }
