/**
 * Letterboxd Review Analytics - Results Page Script
 * Handles display of analysis results and visualizations
 */

document.addEventListener('DOMContentLoaded', function() {
    // Get analysis results from session storage
    const resultsJSON = sessionStorage.getItem('analysisResults');

    if (resultsJSON) {
        try {
            const results = JSON.parse(resultsJSON);
            displayResults(results);

            // Clear session storage after displaying
            // sessionStorage.removeItem('analysisResults');
        } catch (error) {
            console.error('Error parsing results:', error);
            showError('Failed to parse analysis results');
        }
    } else {
        showError('No analysis results found. Please search for a movie first.');
    }
});

/**
 * Display analysis results on the page
 * @param {Object} results - Analysis results from backend
 */
function displayResults(results) {
    const loadingState = document.getElementById('loadingState');
    const resultsSection = document.getElementById('resultsSection');
    const errorState = document.getElementById('errorState');

    if (!results.success) {
        showError(results.error || 'Analysis failed');
        return;
    }

    // Hide loading state
    loadingState.style.display = 'none';

    // Populate movie title and date
    document.getElementById('movieTitle').textContent = results.movie_name;
    document.getElementById('analysisDate').textContent = `Analysis Date: ${results.timestamp}`;

    // Populate statistics
    const stats = results.stats;
    document.getElementById('totalReviews').textContent = stats.total_reviews;
    document.getElementById('avgSentiment').textContent = stats.avg_sentiment.toFixed(3);
    document.getElementById('positiveCount').textContent = stats.positive_reviews;
    document.getElementById('neutralCount').textContent = stats.neutral_reviews;
    document.getElementById('negativeCount').textContent = stats.negative_reviews;

    // Populate sentiment breakdown percentages
    document.getElementById('positivePct').textContent = `${stats.positive_pct}%`;
    document.getElementById('neutralPct').textContent = `${stats.neutral_pct}%`;
    document.getElementById('negativePct').textContent = `${stats.negative_pct}%`;

    // Update progress bars
    updateProgressBar('positiveBar', stats.positive_pct);
    updateProgressBar('neutralBar', stats.neutral_pct);
    updateProgressBar('negativeBar', stats.negative_pct);

    // Display sentiment chart
    const chartImg = document.getElementById('sentimentChart');
    chartImg.src = results.chart_url;
    chartImg.onerror = function() {
        console.error('Failed to load chart image');
        this.style.display = 'none';
    };

    // Populate detail statistics
    document.getElementById('maxSentiment').textContent = stats.max_sentiment.toFixed(3);
    document.getElementById('minSentiment').textContent = stats.min_sentiment.toFixed(3);

    // Display sample reviews
    displaySampleReviews(results.sample_reviews);

    // Show results section
    resultsSection.style.display = 'block';
}

/**
 * Update progress bar width
 * @param {string} elementId - ID of progress bar element
 * @param {number} percentage - Percentage to fill
 */
function updateProgressBar(elementId, percentage) {
    const progressBar = document.getElementById(elementId);
    progressBar.style.width = percentage + '%';

    // Add text if percentage is significant
    if (percentage > 15) {
        progressBar.textContent = percentage + '%';
    }
}

/**
 * Display sample reviews
 * @param {Array} reviews - Array of review objects
 */
function displaySampleReviews(reviews) {
    const reviewsList = document.getElementById('reviewsList');
    reviewsList.innerHTML = '';

    if (!reviews || reviews.length === 0) {
        reviewsList.innerHTML = '<p style="color: #999;">No reviews available</p>';
        return;
    }

    reviews.forEach(review => {
        const reviewItem = document.createElement('div');
        reviewItem.className = 'review-item';

        const sentimentClass = review.sentiment_class || 'neutral';
        const sentimentEmoji = sentimentClass === 'positive' ? '😊' : 
                              sentimentClass === 'negative' ? '😞' : '😐';

        reviewItem.innerHTML = `
            <div class="review-rating">
                ${sentimentEmoji} ${review.rating || 'N/A'} - 
                Score: ${(review.sentiment_score || 0).toFixed(3)}
            </div>
            <div class="review-text">"${truncateText(review.review_text, 150)}"</div>
            <div class="review-meta">
                By ${review.reviewer || 'Anonymous'} • 
                ${review.word_count || 0} words
            </div>
        `;

        reviewsList.appendChild(reviewItem);
    });
}

/**
 * Truncate text to specified length
 * @param {string} text - Text to truncate
 * @param {number} length - Maximum length
 * @returns {string} Truncated text
 */
function truncateText(text, length) {
    if (!text) return '';
    if (text.length <= length) return text;
    return text.substring(0, length) + '...';
}

/**
 * Show error message
 * @param {string} message - Error message to display
 */
function showError(message) {
    const loadingState = document.getElementById('loadingState');
    const errorState = document.getElementById('errorState');
    const errorMessage = document.getElementById('errorMessage');

    loadingState.style.display = 'none';
    errorState.style.display = 'flex';
    errorMessage.textContent = message;
}
