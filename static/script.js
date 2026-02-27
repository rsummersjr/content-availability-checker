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
    document.getElementById('results').classList.add('hidden');
    document.getElementById('error').classList.add('hidden');
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
