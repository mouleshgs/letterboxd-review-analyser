"""
Flask web application for Letterboxd Review Analytics.
Main application file with routes and core functionality.
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import pandas as pd
from datetime import datetime

# Import custom modules
from scraper import scrape_letterboxd_reviews, save_reviews_to_csv, get_sample_reviews
from preprocessor import preprocess_reviews
from analyzer import analyze_all_reviews, calculate_sentiment_stats, get_sentiment_distribution, save_analyzed_reviews
from visualizer import create_sentiment_chart


# Initialize Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'data'

# Create necessary directories if they don't exist
os.makedirs('data', exist_ok=True)
os.makedirs('plots', exist_ok=True)


@app.route('/')
def home():
    """Renders the home page with input form."""
    return render_template('index.html')


@app.route('/api/analyze', methods=['POST'])
def analyze_movie():
    """
    API endpoint for analyzing movie reviews.
    Accepts movie name and performs full analysis pipeline.
    
    Returns:
        JSON response with analysis results
    """
    
    try:
        # Get movie name from request
        data = request.get_json()
        movie_name = data.get('movie_name', '').strip()
        
        if not movie_name:
            return jsonify({'error': 'Movie name is required'}), 400
        
        print(f"\n{'='*60}")
        print(f"📽️  ANALYZING: {movie_name}")
        print(f"{'='*60}")
        
        # Step 1: Scrape reviews
        print("\n[Step 1] Scraping Reviews...")
        raw_filepath = os.path.join('data', 'reviews_raw.csv')
        
        # Try to scrape real reviews, fall back to sample if it fails
        reviews = scrape_letterboxd_reviews(movie_name, max_reviews=50)
        
        if not reviews:
            print("⚠ Using sample reviews (actual scraping unavailable)")
            reviews = get_sample_reviews(movie_name)
        
        if not reviews:
            return jsonify({'error': 'Could not fetch reviews for this movie'}), 400
        
        # Save raw reviews
        save_reviews_to_csv(reviews, raw_filepath)
        
        # Step 2: Preprocess reviews
        print("\n[Step 2] Preprocessing Reviews...")
        clean_filepath = os.path.join('data', 'reviews_clean.csv')
        df_clean = preprocess_reviews(raw_filepath, clean_filepath)
        
        if df_clean is None or len(df_clean) == 0:
            return jsonify({'error': 'No valid reviews after preprocessing'}), 400
        
        # Step 3: Sentiment Analysis
        print("\n[Step 3] Sentiment Analysis...")
        df_analyzed = analyze_all_reviews(df_clean)
        
        # Save analyzed reviews
        analyzed_filepath = os.path.join('data', 'reviews_analyzed.csv')
        save_analyzed_reviews(df_analyzed, analyzed_filepath)
        
        # Step 4: Calculate Statistics
        print("\n[Step 4] Calculating Statistics...")
        sentiment_stats = calculate_sentiment_stats(df_analyzed)
        sentiment_distribution = get_sentiment_distribution(df_analyzed)
        
        # Step 5: Create Visualizations
        print("\n[Step 5] Creating Visualizations...")
        chart_path = os.path.join('plots', f'{movie_name.replace(" ", "_")}_sentiment.png')
        create_sentiment_chart(sentiment_distribution, movie_name, chart_path)
        
        # Prepare response
        print(f"\n{'='*60}")
        print("✓ ANALYSIS COMPLETE!")
        print(f"{'='*60}\n")
        
        response = {
            'success': True,
            'movie_name': movie_name,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'stats': sentiment_stats,
            'sentiment_distribution': sentiment_distribution,
            'chart_url': f'/plots/{os.path.basename(chart_path)}',
            'sample_reviews': df_analyzed.head(5).to_dict('records')
        }
        
        return jsonify(response)
        
    except Exception as e:
        print(f"✗ Error during analysis: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500


@app.route('/results')
def results():
    """Renders the results page."""
    return render_template('results.html')


@app.route('/plots/<filename>')
def serve_plot(filename):
    """Serves plot images from the plots directory."""
    return send_from_directory('plots', filename)


@app.route('/api/health')
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'message': 'Letterboxd Review Analytics is running'})


@app.errorhandler(404)
def page_not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Page not found'}), 404


@app.errorhandler(500)
def internal_server_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    print("🚀 Starting Letterboxd Review Analytics...")
    print("📍 App running at http://localhost:5000")
    print("📝 Press CTRL+C to stop\n")
    
    # Run Flask app in debug mode for development
    app.run(debug=True, port=5000, host='0.0.0.0')
