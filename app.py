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

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    track_name = data.get('track_name', '').strip()
    artist_name = data.get('artist_name', '').strip()

    if not track_name:
        return jsonify({'error': 'Track name is required'}), 400

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

    return jsonify(results)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port)
