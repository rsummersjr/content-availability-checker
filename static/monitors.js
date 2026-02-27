// Toggle email input visibility
document.getElementById('monitor-notify').addEventListener('change', function() {
    const emailGroup = document.getElementById('email-group');
    if (this.checked) {
        emailGroup.style.display = 'block';
    } else {
        emailGroup.style.display = 'none';
    }
});

// Create new monitor
async function createMonitor() {
    const trackName = document.getElementById('monitor-track').value.trim();
    const artistName = document.getElementById('monitor-artist').value.trim();
    const frequency = parseInt(document.getElementById('monitor-frequency').value);
    const country = document.getElementById('monitor-country').value;
    const emailNotify = document.getElementById('monitor-notify').checked;
    const emailAddress = document.getElementById('monitor-email').value.trim();

    // Validation
    if (!trackName) {
        showError('Please enter a track name');
        return;
    }

    if (emailNotify && !emailAddress) {
        showError('Please enter an email address for notifications');
        return;
    }

    if (emailNotify && !isValidEmail(emailAddress)) {
        showError('Please enter a valid email address');
        return;
    }

    try {
        const response = await fetch('/monitors', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                track_name: trackName,
                artist_name: artistName,
                check_frequency_hours: frequency,
                email_notify: emailNotify,
                email_address: emailAddress,
                country_code: country
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to create monitor');
        }

        const data = await response.json();
        showSuccess('Monitor created successfully! Initial check in progress...');
        clearMonitorForm();
        setTimeout(loadMonitors, 2000); // Reload monitors after 2 seconds

    } catch (error) {
        showError(error.message);
    }
}

// Load all monitors
async function loadMonitors() {
    const loading = document.getElementById('monitors-loading');
    const container = document.getElementById('monitors-container');

    loading.classList.remove('hidden');
    container.innerHTML = '';

    try {
        const response = await fetch('/monitors');
        if (!response.ok) throw new Error('Failed to load monitors');

        const data = await response.json();

        loading.classList.add('hidden');

        if (data.monitors.length === 0) {
            container.innerHTML = '<p class="empty-state">No monitors created yet. Create one above to get started!</p>';
            return;
        }

        // Sort monitors: active first, then by creation date
        data.monitors.sort((a, b) => {
            if (a.is_active !== b.is_active) {
                return b.is_active - a.is_active;
            }
            return new Date(b.created_at) - new Date(a.created_at);
        });

        data.monitors.forEach(monitor => {
            container.appendChild(createMonitorCard(monitor));
        });

    } catch (error) {
        loading.classList.add('hidden');
        showError(error.message);
    }
}

// Create monitor card element
function createMonitorCard(monitor) {
    const card = document.createElement('div');
    card.className = 'monitor-card';
    card.id = `monitor-${monitor.id}`;

    const statusClass = monitor.is_active ? 'active' : 'inactive';
    const statusText = monitor.is_active ? 'Active' : 'Inactive';

    let availabilityHTML = '';
    if (monitor.last_state) {
        const platforms = {
            'youtube_music': 'YouTube Music',
            'youtube': 'YouTube',
            'deezer': 'Deezer',
            'apple_music': 'Apple Music',
            'amazon_music': 'Amazon Music',
            'tidal': 'Tidal'
        };

        availabilityHTML = '<div class="monitor-availability"><div class="availability-grid">';
        for (const [key, name] of Object.entries(platforms)) {
            const available = monitor.last_state[key]?.available || false;
            const statusClass = available ? 'available' : 'unavailable';
            const statusIcon = available ? '✓' : '✗';
            availabilityHTML += `
                <div class="platform-status ${statusClass}">
                    <span class="platform-name">${name}</span>
                    ${statusIcon}
                </div>
            `;
        }
        availabilityHTML += '</div></div>';
    }

    card.innerHTML = `
        <div class="monitor-header">
            <div class="monitor-title">
                <h3>${monitor.track_name}</h3>
                <p>${monitor.artist_name || 'No artist specified'}</p>
            </div>
            <div class="monitor-status">
                <span class="status-badge ${statusClass}">${statusText}</span>
            </div>
        </div>

        <div class="monitor-details">
            <div class="detail-item">
                <span class="detail-label">Check Frequency</span>
                <span class="detail-value">Every ${monitor.check_frequency_hours} hour(s)</span>
            </div>
            <div class="detail-item">
                <span class="detail-label">Country</span>
                <span class="detail-value">${monitor.country_code}</span>
            </div>
            <div class="detail-item">
                <span class="detail-label">Email Notifications</span>
                <span class="detail-value">${monitor.email_notify ? `✓ ${monitor.email_address}` : '✗ Disabled'}</span>
            </div>
            <div class="detail-item">
                <span class="detail-label">Last Checked</span>
                <span class="detail-value">${monitor.last_checked ? formatDate(monitor.last_checked) : 'Never'}</span>
            </div>
            <div class="detail-item">
                <span class="detail-label">Next Check</span>
                <span class="detail-value">${monitor.next_check ? formatDate(monitor.next_check) : 'Pending'}</span>
            </div>
            <div class="detail-item">
                <span class="detail-label">Created</span>
                <span class="detail-value">${formatDate(monitor.created_at)}</span>
            </div>
        </div>

        ${availabilityHTML}

        <div class="monitor-actions">
            <button class="btn-action btn-check" onclick="checkMonitorNow(${monitor.id})">
                Check Now
            </button>
            <button class="btn-action btn-toggle" onclick="toggleMonitor(${monitor.id}, ${monitor.is_active})">
                ${monitor.is_active ? 'Pause' : 'Resume'}
            </button>
            <button class="btn-action btn-history" onclick="viewHistory(${monitor.id})">
                View History
            </button>
            <button class="btn-action btn-delete" onclick="deleteMonitor(${monitor.id})">
                Delete
            </button>
        </div>
    `;

    return card;
}

// Check monitor now
async function checkMonitorNow(monitorId) {
    try {
        showSuccess('Running check...');

        const response = await fetch(`/monitors/${monitorId}/check-now`, {
            method: 'POST'
        });

        if (!response.ok) throw new Error('Failed to run check');

        const data = await response.json();

        if (data.result.changes && data.result.changes.length > 0) {
            showSuccess(`Check complete! ${data.result.changes.length} change(s) detected.`);
        } else {
            showSuccess('Check complete! No changes detected.');
        }

        setTimeout(loadMonitors, 1000);

    } catch (error) {
        showError(error.message);
    }
}

// Toggle monitor active status
async function toggleMonitor(monitorId, currentlyActive) {
    try {
        const response = await fetch(`/monitors/${monitorId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                is_active: !currentlyActive
            })
        });

        if (!response.ok) throw new Error('Failed to update monitor');

        showSuccess(`Monitor ${currentlyActive ? 'paused' : 'resumed'} successfully`);
        setTimeout(loadMonitors, 500);

    } catch (error) {
        showError(error.message);
    }
}

// Delete monitor
async function deleteMonitor(monitorId) {
    if (!confirm('Are you sure you want to delete this monitor? This action cannot be undone.')) {
        return;
    }

    try {
        const response = await fetch(`/monitors/${monitorId}`, {
            method: 'DELETE'
        });

        if (!response.ok) throw new Error('Failed to delete monitor');

        showSuccess('Monitor deleted successfully');
        setTimeout(loadMonitors, 500);

    } catch (error) {
        showError(error.message);
    }
}

// View history
async function viewHistory(monitorId) {
    try {
        const response = await fetch(`/monitors/${monitorId}/checks?limit=20`);
        if (!response.ok) throw new Error('Failed to load history');

        const data = await response.json();

        // Create a simple history view (you can enhance this)
        let historyHTML = `
            <h3>Check History (Last 20 checks)</h3>
            <p>Monitor ID: ${monitorId}</p>
            <div style="max-height: 400px; overflow-y: auto; margin-top: 20px;">
        `;

        if (data.checks.length === 0) {
            historyHTML += '<p>No checks recorded yet.</p>';
        } else {
            data.checks.forEach(check => {
                const changesCount = check.changes_detected ? check.changes_detected.length : 0;
                const changesText = changesCount > 0 ? `${changesCount} change(s) detected` : 'No changes';

                historyHTML += `
                    <div style="background: #f9fafb; padding: 10px; margin-bottom: 10px; border-radius: 6px;">
                        <strong>${formatDate(check.checked_at)}</strong><br>
                        ${changesText}
                        ${check.notification_sent ? ' - Email sent ✓' : ''}
                    </div>
                `;
            });
        }

        historyHTML += '</div>';

        // Show in success message area (you can create a modal instead)
        const successDiv = document.getElementById('success');
        successDiv.innerHTML = historyHTML;
        successDiv.classList.remove('hidden');
        successDiv.scrollIntoView({ behavior: 'smooth' });

    } catch (error) {
        showError(error.message);
    }
}

// Helper functions
function clearMonitorForm() {
    document.getElementById('monitor-track').value = '';
    document.getElementById('monitor-artist').value = '';
    document.getElementById('monitor-frequency').value = '6';
    document.getElementById('monitor-country').value = 'US';
    document.getElementById('monitor-notify').checked = false;
    document.getElementById('monitor-email').value = '';
    document.getElementById('email-group').style.display = 'none';
}

function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function formatDate(dateString) {
    if (!dateString) return 'Never';

    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins} min${diffMins > 1 ? 's' : ''} ago`;
    if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
    if (diffDays < 7) return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;

    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function showError(message) {
    const errorDiv = document.getElementById('error');
    const successDiv = document.getElementById('success');

    successDiv.classList.add('hidden');
    errorDiv.textContent = message;
    errorDiv.classList.remove('hidden');
    errorDiv.scrollIntoView({ behavior: 'smooth' });

    setTimeout(() => {
        errorDiv.classList.add('hidden');
    }, 5000);
}

function showSuccess(message) {
    const successDiv = document.getElementById('success');
    const errorDiv = document.getElementById('error');

    errorDiv.classList.add('hidden');
    successDiv.textContent = message;
    successDiv.classList.remove('hidden');
    successDiv.scrollIntoView({ behavior: 'smooth' });

    setTimeout(() => {
        successDiv.classList.add('hidden');
    }, 5000);
}

// Load monitors on page load
document.addEventListener('DOMContentLoaded', function() {
    loadMonitors();
});
