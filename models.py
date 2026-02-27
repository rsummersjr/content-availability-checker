from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Monitor(db.Model):
    """Model for content availability monitors"""
    id = db.Column(db.Integer, primary_key=True)
    track_name = db.Column(db.String(200), nullable=False)
    artist_name = db.Column(db.String(200), nullable=True)
    check_frequency_hours = db.Column(db.Integer, nullable=False, default=6)
    email_notify = db.Column(db.Boolean, default=False)
    email_address = db.Column(db.String(200), nullable=True)
    country_code = db.Column(db.String(10), default='US')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_checked = db.Column(db.DateTime, nullable=True)
    next_check = db.Column(db.DateTime, nullable=True)

    # Store the last known state as JSON
    last_state = db.Column(db.Text, nullable=True)

    # Relationship to check history
    checks = db.relationship('MonitorCheck', backref='monitor', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'track_name': self.track_name,
            'artist_name': self.artist_name,
            'check_frequency_hours': self.check_frequency_hours,
            'email_notify': self.email_notify,
            'email_address': self.email_address,
            'country_code': self.country_code,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_checked': self.last_checked.isoformat() if self.last_checked else None,
            'next_check': self.next_check.isoformat() if self.next_check else None,
            'last_state': json.loads(self.last_state) if self.last_state else None
        }

class MonitorCheck(db.Model):
    """Model for individual monitor check results"""
    id = db.Column(db.Integer, primary_key=True)
    monitor_id = db.Column(db.Integer, db.ForeignKey('monitor.id'), nullable=False)
    checked_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Store availability state as JSON
    availability_state = db.Column(db.Text, nullable=False)

    # Store any changes detected
    changes_detected = db.Column(db.Text, nullable=True)

    # Whether notification was sent
    notification_sent = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'monitor_id': self.monitor_id,
            'checked_at': self.checked_at.isoformat() if self.checked_at else None,
            'availability_state': json.loads(self.availability_state) if self.availability_state else None,
            'changes_detected': json.loads(self.changes_detected) if self.changes_detected else None,
            'notification_sent': self.notification_sent
        }
