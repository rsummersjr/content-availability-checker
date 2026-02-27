async function searchTrack() {
    const trackName = document.getElementById('track-name').value.trim();
    const artistName = document.getElementById('artist-name').value.trim();

    if (!trackName) {
        alert('Please enter a track name');
        return;
    }

    // Show loading, hide results and errors
    document.getElementById('loading').classList.remove('hidden');
    document.getElementById('results').classList.add('hidden');
    document.getElementById('error').classList.add('hidden');

    try {
        const response = await fetch('/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                track_name: trackName,
                artist_name: artistName
            })
        });

        if (!response.ok) {
            throw new Error('Search request failed');
        }

        const data = await response.json();
        displayResults(data);

    } catch (error) {
        document.getElementById('loading').classList.add('hidden');
        const errorDiv = document.getElementById('error');
        errorDiv.textContent = `Error: ${error.message}`;
        errorDiv.classList.remove('hidden');
    }
}

function displayResults(data) {
    document.getElementById('loading').classList.add('hidden');
    document.getElementById('results').classList.remove('hidden');

    // Display query info
    document.getElementById('result-track').textContent = data.query.track;
    document.getElementById('result-artist').textContent = data.query.artist;

    // Display platform results
    displayPlatform('youtube-music', data.platforms.youtube_music);
    displayPlatform('youtube', data.platforms.youtube);
    displayPlatform('deezer', data.platforms.deezer);
    displayPlatform('apple-music', data.platforms.apple_music);
    displayPlatform('amazon-music', data.platforms.amazon_music);
    displayPlatform('tidal', data.platforms.tidal);
}

function formatDate(dateString) {
    if (!dateString) return null;

    try {
        const date = new Date(dateString);
        if (isNaN(date.getTime())) return null;

        const options = { year: 'numeric', month: 'long', day: 'numeric' };
        return date.toLocaleDateString('en-US', options);
    } catch (e) {
        return null;
    }
}

function displayPlatform(platformId, platformData) {
    const card = document.getElementById(`${platformId}-card`);
    const badge = card.querySelector('.status-badge');
    const content = card.querySelector('.platform-content');

    // Clear previous content
    content.innerHTML = '';

    if (platformData.available) {
        // Platform has results
        badge.textContent = '✓ Available';
        badge.className = 'status-badge available';

        if (platformData.results && platformData.results.length > 0) {
            content.innerHTML = `<p style="margin-bottom: 15px; font-weight: 600;">Found ${platformData.count} result(s)</p>`;

            platformData.results.forEach(result => {
                const resultDiv = document.createElement('div');
                resultDiv.className = 'track-result';

                let html = `<h4>${result.title}</h4>`;

                if (result.artist) {
                    html += `<p>Artist: ${result.artist}</p>`;
                }

                if (result.album) {
                    html += `<p>Album: ${result.album}</p>`;
                }

                if (result.channel) {
                    html += `<p>Channel: ${result.channel}</p>`;
                }

                if (result.published_date) {
                    const formattedDate = formatDate(result.published_date);
                    if (formattedDate) {
                        html += `<p class="published-date">📅 Published: ${formattedDate}</p>`;
                    }
                }

                if (result.url) {
                    html += `<a href="${result.url}" target="_blank">Open ➜</a>`;
                }

                resultDiv.innerHTML = html;
                content.appendChild(resultDiv);
            });
        }
    } else if (platformData.setup_required) {
        // Platform requires setup
        badge.textContent = '⚙ Setup Required';
        badge.className = 'status-badge setup-required';

        content.innerHTML = `<p class="error-message">${platformData.error || 'API configuration required'}</p>`;

        if (platformData.note) {
            content.innerHTML += `<p class="note-message">${platformData.note}</p>`;
        }

        if (platformData.manual_search_url) {
            content.innerHTML += `<div class="manual-link"><a href="${platformData.manual_search_url}" target="_blank">Search Manually ➜</a></div>`;
        }
    } else {
        // Platform unavailable or error
        badge.textContent = '✗ Not Found';
        badge.className = 'status-badge unavailable';

        if (platformData.error) {
            content.innerHTML = `<p class="error-message">${platformData.error}</p>`;
        } else {
            content.innerHTML = `<p>No results found</p>`;
        }

        if (platformData.manual_search_url) {
            content.innerHTML += `<div class="manual-link"><a href="${platformData.manual_search_url}" target="_blank">Search Manually ➜</a></div>`;
        }
    }
}

function clearResults() {
    document.getElementById('track-name').value = '';
    document.getElementById('artist-name').value = '';
    document.getElementById('bulk-input').value = '';
    document.getElementById('results').classList.add('hidden');
    document.getElementById('bulk-results').classList.add('hidden');
    document.getElementById('error').classList.add('hidden');
}

// Mode switching
function switchMode(mode) {
    const singleForm = document.getElementById('single-search-form');
    const bulkForm = document.getElementById('bulk-search-form');
    const modeButtons = document.querySelectorAll('.mode-btn');

    // Clear results when switching modes
    clearResults();

    if (mode === 'single') {
        singleForm.classList.remove('hidden');
        bulkForm.classList.add('hidden');
        modeButtons[0].classList.add('active');
        modeButtons[1].classList.remove('active');
    } else {
        singleForm.classList.add('hidden');
        bulkForm.classList.remove('hidden');
        modeButtons[0].classList.remove('active');
        modeButtons[1].classList.add('active');
    }
}

// Store bulk results for detailed view
let bulkSearchResults = [];

// Parse bulk input
function parseBulkInput(input) {
    const lines = input.split('\n').filter(line => line.trim());
    const searches = [];

    lines.forEach(line => {
        const parts = line.split(',').map(p => p.trim());
        if (parts.length >= 1 && parts[0]) {
            searches.push({
                track_name: parts[0],
                artist_name: parts[1] || ''
            });
        }
    });

    return searches;
}

// Bulk search
async function bulkSearchTracks() {
    const bulkInput = document.getElementById('bulk-input').value.trim();

    if (!bulkInput) {
        alert('Please enter at least one track');
        return;
    }

    const searches = parseBulkInput(bulkInput);

    if (searches.length === 0) {
        alert('No valid tracks found. Please check your format.');
        return;
    }

    // Show loading
    document.getElementById('loading').classList.remove('hidden');
    document.getElementById('loading-text').textContent = `Searching for ${searches.length} track(s) across platforms...`;
    document.getElementById('bulk-results').classList.add('hidden');
    document.getElementById('results').classList.add('hidden');
    document.getElementById('error').classList.add('hidden');

    try {
        const response = await fetch('/bulk-search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                searches: searches
            })
        });

        if (!response.ok) {
            throw new Error('Bulk search request failed');
        }

        const data = await response.json();
        bulkSearchResults = data.results;
        displayBulkResults(data);

    } catch (error) {
        document.getElementById('loading').classList.add('hidden');
        const errorDiv = document.getElementById('error');
        errorDiv.textContent = `Error: ${error.message}`;
        errorDiv.classList.remove('hidden');
    }
}

// Display bulk results in table
function displayBulkResults(data) {
    document.getElementById('loading').classList.add('hidden');
    document.getElementById('bulk-results').classList.remove('hidden');

    // Update count
    document.getElementById('bulk-count').textContent = data.total;

    // Build table
    const tbody = document.getElementById('bulk-table-body');
    tbody.innerHTML = '';

    data.results.forEach((result, index) => {
        const row = document.createElement('tr');

        // Track name
        const trackCell = document.createElement('td');
        trackCell.textContent = result.query.track;
        row.appendChild(trackCell);

        // Artist name
        const artistCell = document.createElement('td');
        artistCell.textContent = result.query.artist;
        row.appendChild(artistCell);

        // Platform availability cells
        const platforms = ['youtube_music', 'youtube', 'deezer', 'apple_music', 'amazon_music', 'tidal'];
        platforms.forEach(platform => {
            const cell = document.createElement('td');
            const platformData = result.platforms[platform];

            if (platformData.available) {
                cell.innerHTML = '<span class="availability-yes">Yes</span>';
            } else if (platformData.setup_required) {
                cell.innerHTML = '<span class="availability-setup">Setup</span>';
            } else {
                cell.innerHTML = '<span class="availability-no">No</span>';
            }

            row.appendChild(cell);
        });

        // Details link
        const detailsCell = document.createElement('td');
        const detailsLink = document.createElement('a');
        detailsLink.href = '#';
        detailsLink.className = 'details-link';
        detailsLink.textContent = 'View Details';
        detailsLink.onclick = (e) => {
            e.preventDefault();
            showDetailedView(index);
        };
        detailsCell.appendChild(detailsLink);
        row.appendChild(detailsCell);

        tbody.appendChild(row);
    });
}

// Show detailed view for a specific search from bulk results
function showDetailedView(index) {
    const result = bulkSearchResults[index];

    // Hide bulk results, show detailed results
    document.getElementById('bulk-results').classList.add('hidden');
    document.getElementById('results').classList.remove('hidden');

    // Scroll to results
    document.getElementById('results').scrollIntoView({ behavior: 'smooth' });

    // Display the detailed results
    displayResults(result);
}

// Allow Enter key to trigger search
document.getElementById('track-name').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        searchTrack();
    }
});

document.getElementById('artist-name').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        searchTrack();
    }
});
