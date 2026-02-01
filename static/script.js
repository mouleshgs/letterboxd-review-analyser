/**
 * Letterboxd Review Analytics - Frontend Script
 * Handles form submission and navigation to results page
 */

document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('searchForm');
    const movieNameInput = document.getElementById('movieName');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const btnText = document.querySelector('.btn-text');
    const btnLoader = document.getElementById('btnLoader');
    const errorMessage = document.getElementById('errorMessage');

    // Form submission handler
    searchForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        const movieName = movieNameInput.value.trim();

        // Validation
        if (!movieName) {
            showError('Please enter a movie name');
            return;
        }

        // Disable button and show loader
        analyzeBtn.disabled = true;
        btnText.style.display = 'none';
        btnLoader.style.display = 'inline-flex';
        errorMessage.style.display = 'none';

        try {
            // Send analysis request to backend
            const response = await fetch('/api/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    movie_name: movieName
                })
            });

            const data = await response.json();

            if (response.ok) {
                // Store results in session storage for results page
                sessionStorage.setItem('analysisResults', JSON.stringify(data));

                // Redirect to results page
                window.location.href = '/results';
            } else {
                // Show error message
                showError(data.error || 'An error occurred during analysis');
                resetButton();
            }
        } catch (error) {
            console.error('Error:', error);
            showError('Failed to connect to the server. Please try again.');
            resetButton();
        }
    });

    // Show error message
    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.style.display = 'block';
    }

    // Reset button state
    function resetButton() {
        analyzeBtn.disabled = false;
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
    }

    // Clear error message when user starts typing
    movieNameInput.addEventListener('input', function() {
        errorMessage.style.display = 'none';
    });
});
