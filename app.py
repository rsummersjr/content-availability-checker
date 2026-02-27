from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from api_clients.youtube_client import YouTubeClient
from api_clients.deezer_client import DeezerClient
from api_clients.apple_music_client import AppleMusicClient
from api_clients.amazon_music_client import AmazonMusicClient
from api_clients.tidal_client import TidalClient

# Load environment variables from .env file (for local development)
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize API clients
youtube_client = YouTubeClient(api_key=os.getenv('YOUTUBE_API_KEY'))
deezer_client = DeezerClient()
apple_music_client = AppleMusicClient(api_key=os.getenv('APPLE_MUSIC_API_KEY'))
amazon_music_client = AmazonMusicClient()
tidal_client = TidalClient()

@app.route('/')
def index():
    return render_template('index.html')

def search_single_track(track_name, artist_name):
    """Search for a single track across all platforms"""
    results = {
        'query': {
            'track': track_name,
            'artist': artist_name if artist_name else 'Not specified'
        },
        'platforms': {}
    }

    # Search YouTube Music & YouTube
    youtube_results = youtube_client.search(track_name, artist_name)
    results['platforms']['youtube_music'] = youtube_results.get('youtube_music', {})
    results['platforms']['youtube'] = youtube_results.get('youtube', {})

    # Search Deezer
    results['platforms']['deezer'] = deezer_client.search(track_name, artist_name)

    # Search Apple Music
    results['platforms']['apple_music'] = apple_music_client.search(track_name, artist_name)

    # Search Amazon Music
    results['platforms']['amazon_music'] = amazon_music_client.search(track_name, artist_name)

    # Search Tidal
    results['platforms']['tidal'] = tidal_client.search(track_name, artist_name)

    return results

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    track_name = data.get('track_name', '').strip()
    artist_name = data.get('artist_name', '').strip()

    if not track_name:
        return jsonify({'error': 'Track name is required'}), 400

    return jsonify(search_single_track(track_name, artist_name))

@app.route('/bulk-search', methods=['POST'])
def bulk_search():
    data = request.json
    searches = data.get('searches', [])

    if not searches or not isinstance(searches, list):
        return jsonify({'error': 'Searches array is required'}), 400

    results = []

    for idx, search_item in enumerate(searches):
        track_name = search_item.get('track_name', '').strip()
        artist_name = search_item.get('artist_name', '').strip()

        if not track_name:
            continue  # Skip empty entries

        # Perform search for this track
        search_result = search_single_track(track_name, artist_name)

        # Add search ID for linking to detailed view
        search_result['search_id'] = idx
        results.append(search_result)

    return jsonify({
        'total': len(results),
        'results': results
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port)
