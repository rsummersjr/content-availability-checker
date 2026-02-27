import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from models import db, Monitor, MonitorCheck
import os

def send_email_notification(to_email, track_name, artist_name, changes):
    """Send email notification about availability changes"""
    from_email = os.getenv('SMTP_FROM_EMAIL', 'noreply@musictrackfinder.com')
    smtp_server = os.getenv('SMTP_SERVER', 'localhost')
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    smtp_username = os.getenv('SMTP_USERNAME', '')
    smtp_password = os.getenv('SMTP_PASSWORD', '')

    # Create email content
    subject = f"Content Availability Change Alert: {track_name}"

    html_body = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; text-align: center; }}
            .content {{ padding: 20px; }}
            .track-info {{ background: #f9fafb; padding: 15px; border-radius: 8px; margin: 20px 0; }}
            .changes {{ margin: 20px 0; }}
            .change-item {{ background: #fff; border-left: 4px solid #667eea; padding: 10px; margin: 10px 0; }}
            .platform {{ font-weight: bold; color: #667eea; }}
            .status-change {{ color: #10b981; }}
            .status-removed {{ color: #ef4444; }}
            .footer {{ text-align: center; padding: 20px; color: #666; font-size: 0.9rem; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🎵 Content Availability Alert</h1>
        </div>
        <div class="content">
            <p>Hello,</p>
            <p>We detected changes in the availability of content you're monitoring:</p>

            <div class="track-info">
                <strong>Track:</strong> {track_name}<br>
                <strong>Artist:</strong> {artist_name or 'Not specified'}<br>
                <strong>Checked:</strong> {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}
            </div>

            <div class="changes">
                <h3>Changes Detected:</h3>
    """

    for change in changes:
        platform = change['platform']
        change_type = change['type']

        if change_type == 'now_available':
            html_body += f"""
                <div class="change-item">
                    <span class="platform">{platform}</span>:
                    <span class="status-change">✅ Content is now available</span>
                </div>
            """
        elif change_type == 'no_longer_available':
            html_body += f"""
                <div class="change-item">
                    <span class="platform">{platform}</span>:
                    <span class="status-removed">❌ Content is no longer available</span>
                </div>
            """

    html_body += """
            </div>

            <p>You can view the full details by visiting the Music Track Finder application.</p>
        </div>
        <div class="footer">
            <p>This is an automated notification from Music Track Finder.</p>
            <p>To manage your monitors, visit the application dashboard.</p>
        </div>
    </body>
    </html>
    """

    # Create message
    message = MIMEMultipart('alternative')
    message['Subject'] = subject
    message['From'] = from_email
    message['To'] = to_email

    # Plain text version
    text_body = f"""
Content Availability Alert

Track: {track_name}
Artist: {artist_name or 'Not specified'}
Checked: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}

Changes Detected:
"""
    for change in changes:
        status = '✅ Now available' if change['type'] == 'now_available' else '❌ No longer available'
        text_body += f"\n{change['platform']}: {status}"

    text_body += "\n\nThis is an automated notification from Music Track Finder."

    # Attach both parts
    message.attach(MIMEText(text_body, 'plain'))
    message.attach(MIMEText(html_body, 'html'))

    # Send email
    try:
        # Try to send via SMTP if configured
        if smtp_username and smtp_password:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.send_message(message)
            print(f"✅ Email sent to {to_email}")
            return True
        else:
            # If no SMTP configured, just log it (for development)
            print(f"📧 [EMAIL SIMULATION] Would send to {to_email}:")
            print(text_body)
            return True
    except Exception as e:
        print(f"❌ Failed to send email: {str(e)}")
        return False


def detect_changes(old_state, new_state):
    """Compare two availability states and detect changes"""
    changes = []

    platforms = ['youtube_music', 'youtube', 'deezer', 'apple_music', 'amazon_music', 'tidal']

    for platform in platforms:
        old_available = old_state.get(platform, {}).get('available', False) if old_state else False
        new_available = new_state.get(platform, {}).get('available', False)

        # Check if status changed
        if old_available != new_available:
            if new_available:
                changes.append({
                    'platform': platform.replace('_', ' ').title(),
                    'type': 'now_available'
                })
            else:
                changes.append({
                    'platform': platform.replace('_', ' ').title(),
                    'type': 'no_longer_available'
                })

    return changes


def perform_monitor_check(monitor, search_function):
    """Perform a single monitor check"""
    from datetime import datetime

    # Perform search
    result = search_function(monitor.track_name, monitor.artist_name)

    # Extract availability state
    availability_state = {
        'youtube_music': {'available': result['platforms']['youtube_music'].get('available', False)},
        'youtube': {'available': result['platforms']['youtube'].get('available', False)},
        'deezer': {'available': result['platforms']['deezer'].get('available', False)},
        'apple_music': {'available': result['platforms']['apple_music'].get('available', False)},
        'amazon_music': {'available': result['platforms']['amazon_music'].get('available', False)},
        'tidal': {'available': result['platforms']['tidal'].get('available', False)}
    }

    # Detect changes
    old_state = json.loads(monitor.last_state) if monitor.last_state else None
    changes = detect_changes(old_state, availability_state)

    # Create check record
    check = MonitorCheck(
        monitor_id=monitor.id,
        checked_at=datetime.utcnow(),
        availability_state=json.dumps(availability_state),
        changes_detected=json.dumps(changes) if changes else None,
        notification_sent=False
    )

    # Send notification if changes detected and email enabled
    if changes and monitor.email_notify and monitor.email_address:
        notification_sent = send_email_notification(
            monitor.email_address,
            monitor.track_name,
            monitor.artist_name,
            changes
        )
        check.notification_sent = notification_sent

    # Update monitor
    monitor.last_checked = datetime.utcnow()
    monitor.last_state = json.dumps(availability_state)
    monitor.next_check = datetime.utcnow() + timedelta(hours=monitor.check_frequency_hours)

    # Save to database
    db.session.add(check)
    db.session.commit()

    return {
        'monitor_id': monitor.id,
        'checked_at': check.checked_at,
        'changes': changes,
        'notification_sent': check.notification_sent
    }


def check_all_due_monitors(app, search_function):
    """Check all monitors that are due for a check"""
    with app.app_context():
        now = datetime.utcnow()

        # Find all active monitors that are due for checking
        monitors = Monitor.query.filter(
            Monitor.is_active == True,
            db.or_(
                Monitor.next_check == None,
                Monitor.next_check <= now
            )
        ).all()

        print(f"🔍 Checking {len(monitors)} monitors...")

        results = []
        for monitor in monitors:
            try:
                result = perform_monitor_check(monitor, search_function)
                results.append(result)
                print(f"✅ Checked: {monitor.track_name} - {len(result['changes'])} changes detected")
            except Exception as e:
                print(f"❌ Error checking {monitor.track_name}: {str(e)}")

        return results
