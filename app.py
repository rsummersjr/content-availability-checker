from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from api_clients.youtube_client import YouTubeClient
from api_clients.deezer_client import DeezerClient
from api_clients.apple_music_client import AppleMusicClient
from api_clients.amazon_music_client import AmazonMusicClient
from api_clients.tidal_client import TidalClient
from models import db, Monitor, MonitorCheck
from monitor_service import check_all_due_monitors, perform_monitor_check

# Load environment variables from .env file (for local development)
load_dotenv()

app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///monitors.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

# Initialize API clients
youtube_client = YouTubeClient(api_key=os.getenv('YOUTUBE_API_KEY'))
deezer_client = DeezerClient()
apple_music_client = AppleMusicClient(api_key=os.getenv('APPLE_MUSIC_API_KEY'))
amazon_music_client = AmazonMusicClient()
tidal_client = TidalClient()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/monitors-page')
def monitors_page():
    return render_template('monitors.html')

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

# Monitor Management Endpoints

@app.route('/monitors', methods=['GET'])
def get_monitors():
    """Get all monitors"""
    monitors = Monitor.query.all()
    return jsonify({
        'total': len(monitors),
        'monitors': [m.to_dict() for m in monitors]
    })

@app.route('/monitors', methods=['POST'])
def create_monitor():
    """Create a new monitor"""
    data = request.json

    track_name = data.get('track_name', '').strip()
    if not track_name:
        return jsonify({'error': 'Track name is required'}), 400

    # Validate email if notifications enabled
    if data.get('email_notify') and not data.get('email_address'):
        return jsonify({'error': 'Email address required for notifications'}), 400

    monitor = Monitor(
        track_name=track_name,
        artist_name=data.get('artist_name', '').strip(),
        check_frequency_hours=data.get('check_frequency_hours', 6),
        email_notify=data.get('email_notify', False),
        email_address=data.get('email_address', '').strip(),
        country_code=data.get('country_code', 'US'),
        is_active=True,
        next_check=datetime.utcnow()  # Check immediately on creation
    )

    db.session.add(monitor)
    db.session.commit()

    # Perform initial check
    try:
        perform_monitor_check(monitor, search_single_track)
    except Exception as e:
        print(f"Error performing initial check: {str(e)}")

    return jsonify({
        'message': 'Monitor created successfully',
        'monitor': monitor.to_dict()
    }), 201

@app.route('/monitors/<int:monitor_id>', methods=['GET'])
def get_monitor(monitor_id):
    """Get a specific monitor"""
    monitor = Monitor.query.get_or_404(monitor_id)
    return jsonify(monitor.to_dict())

@app.route('/monitors/<int:monitor_id>', methods=['PUT'])
def update_monitor(monitor_id):
    """Update a monitor"""
    monitor = Monitor.query.get_or_404(monitor_id)
    data = request.json

    if 'track_name' in data:
        monitor.track_name = data['track_name'].strip()
    if 'artist_name' in data:
        monitor.artist_name = data['artist_name'].strip()
    if 'check_frequency_hours' in data:
        monitor.check_frequency_hours = data['check_frequency_hours']
    if 'email_notify' in data:
        monitor.email_notify = data['email_notify']
    if 'email_address' in data:
        monitor.email_address = data['email_address'].strip()
    if 'country_code' in data:
        monitor.country_code = data['country_code']
    if 'is_active' in data:
        monitor.is_active = data['is_active']

    db.session.commit()

    return jsonify({
        'message': 'Monitor updated successfully',
        'monitor': monitor.to_dict()
    })

@app.route('/monitors/<int:monitor_id>', methods=['DELETE'])
def delete_monitor(monitor_id):
    """Delete a monitor"""
    monitor = Monitor.query.get_or_404(monitor_id)
    db.session.delete(monitor)
    db.session.commit()

    return jsonify({'message': 'Monitor deleted successfully'})

@app.route('/monitors/<int:monitor_id>/checks', methods=['GET'])
def get_monitor_checks(monitor_id):
    """Get check history for a monitor"""
    monitor = Monitor.query.get_or_404(monitor_id)
    limit = request.args.get('limit', 10, type=int)

    checks = MonitorCheck.query.filter_by(monitor_id=monitor_id)\
        .order_by(MonitorCheck.checked_at.desc())\
        .limit(limit)\
        .all()

    return jsonify({
        'monitor_id': monitor_id,
        'total': len(checks),
        'checks': [c.to_dict() for c in checks]
    })

@app.route('/monitors/<int:monitor_id>/check-now', methods=['POST'])
def check_monitor_now(monitor_id):
    """Manually trigger a check for a monitor"""
    monitor = Monitor.query.get_or_404(monitor_id)

    try:
        result = perform_monitor_check(monitor, search_single_track)
        return jsonify({
            'message': 'Check completed successfully',
            'result': result
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Initialize scheduler
scheduler = BackgroundScheduler()

def scheduled_monitor_check():
    """Function to be called by scheduler"""
    check_all_due_monitors(app, search_single_track)

# Add job to check monitors every hour
scheduler.add_job(
    func=scheduled_monitor_check,
    trigger="interval",
    hours=1,
    id='monitor_check',
    replace_existing=True
)

# Start scheduler
if not scheduler.running:
    scheduler.start()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port)
