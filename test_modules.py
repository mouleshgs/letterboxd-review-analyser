"""
Sample test script demonstrating how to use the modules directly.
Run this to test functionality without the web server.
"""

import os
import pandas as pd
from scraper import scrape_letterboxd_reviews, save_reviews_to_csv, get_sample_reviews
from preprocessor import preprocess_reviews
from analyzer import analyze_all_reviews, calculate_sentiment_stats, get_sentiment_distribution
from visualizer import create_sentiment_chart


def test_full_pipeline():
    """
    Tests the complete analysis pipeline with a sample movie.
    """
    
    movie_name = "Inception"
    print(f"\n{'='*60}")
    print(f"Testing Pipeline for: {movie_name}")
    print(f"{'='*60}\n")
    
    # Create necessary directories
    os.makedirs('data', exist_ok=True)
    os.makedirs('plots', exist_ok=True)
    
    # Step 1: Get Reviews
    print("[Step 1] Fetching Reviews...")
    print("-" * 60)
    
    # Use sample reviews for testing
    reviews = get_sample_reviews(movie_name)
    print(f"✓ Fetched {len(reviews)} reviews\n")
    
    # Step 2: Save Raw Reviews
    print("[Step 2] Saving Raw Reviews...")
    print("-" * 60)
    
    raw_filepath = os.path.join('data', f'{movie_name}_reviews_raw.csv')
    save_reviews_to_csv(reviews, raw_filepath)
    print(f"✓ Raw reviews saved\n")
    
    # Step 3: Preprocess Reviews
    print("[Step 3] Preprocessing Reviews...")
    print("-" * 60)
    
    clean_filepath = os.path.join('data', f'{movie_name}_reviews_clean.csv')
    df_clean = preprocess_reviews(raw_filepath, clean_filepath)
    
    if df_clean is not None:
        print(f"✓ Data preview:")
        print(df_clean.head())
        print()
    
    # Step 4: Sentiment Analysis
    print("[Step 4] Performing Sentiment Analysis...")
    print("-" * 60)
    
    df_analyzed = analyze_all_reviews(df_clean)
    
    print("\n✓ Sentiment analysis preview:")
    print(df_analyzed[['review_text', 'sentiment_score', 'sentiment_class']].head())
    print()
    
    # Step 5: Calculate Statistics
    print("[Step 5] Calculating Statistics...")
    print("-" * 60)
    
    stats = calculate_sentiment_stats(df_analyzed)
    
    print("✓ Sentiment Statistics:")
    for key, value in stats.items():
        print(f"   {key}: {value}")
    print()
    
    # Step 6: Get Sentiment Distribution
    print("[Step 6] Getting Sentiment Distribution...")
    print("-" * 60)
    
    distribution = get_sentiment_distribution(df_analyzed)
    print(f"✓ Distribution: {distribution}\n")
    
    # Step 7: Create Visualization
    print("[Step 7] Creating Visualization...")
    print("-" * 60)
    
    chart_path = os.path.join('plots', f'{movie_name}_sentiment.png')
    create_sentiment_chart(distribution, movie_name, chart_path)
    print()
    
    # Final Summary
    print(f"{'='*60}")
    print("Analysis Complete!")
    print(f"{'='*60}")
    print(f"\nFiles created:")
    print(f"  - {raw_filepath}")
    print(f"  - {clean_filepath}")
    print(f"  - {chart_path}")
    print(f"\nTo view the web interface, run:")
    print(f"  python app.py")
    print()


def test_preprocessing():
    """
    Tests just the preprocessing module.
    """
    
    print("\n" + "="*60)
    print("Testing Preprocessing Module")
    print("="*60 + "\n")
    
    from preprocessor import clean_text, count_words
    
    # Test text cleaning
    test_text = "Check out this link: https://example.com! #amazing @user123 :)"
    cleaned = clean_text(test_text)
    
    print("Original text:")
    print(f"  {test_text}\n")
    print("Cleaned text:")
    print(f"  {cleaned}\n")
    
    # Test word counting
    words = count_words(cleaned)
    print(f"Word count: {words}\n")


def test_sentiment_analysis():
    """
    Tests just the sentiment analysis module.
    """
    
    print("\n" + "="*60)
    print("Testing Sentiment Analysis Module")
    print("="*60 + "\n")
    
    from analyzer import initialize_sentiment_analyzer, analyze_sentiment
    
    # Initialize analyzer
    analyzer = initialize_sentiment_analyzer()
    
    # Test samples
    test_reviews = [
        "This movie is absolutely amazing! I loved every second.",
        "It was okay, nothing special really.",
        "Terrible waste of time. One of the worst films I've seen."
    ]
    
    for review in test_reviews:
        score = analyze_sentiment(review, analyzer)
        print(f"Review: {review}")
        print(f"Sentiment Score: {score:.3f}")
        print()


def test_visualization():
    """
    Tests the visualization module.
    """
    
    print("\n" + "="*60)
    print("Testing Visualization Module")
    print("="*60 + "\n")
    
    os.makedirs('plots', exist_ok=True)
    
    # Sample sentiment distribution
    sentiment_dist = {
        'positive': 45,
        'neutral': 20,
        'negative': 35
    }
    
    from visualizer import create_sentiment_chart
    
    chart_path = 'plots/test_sentiment.png'
    create_sentiment_chart(sentiment_dist, "Test Movie", chart_path)
    
    if os.path.exists(chart_path):
        print(f"✓ Chart created successfully: {chart_path}\n")
    else:
        print(f"✗ Failed to create chart\n")


if __name__ == '__main__':
    import sys
    
    print("\n" + "="*60)
    print("Letterboxd Review Analytics - Test Suite")
    print("="*60)
    
    if len(sys.argv) > 1:
        test_type = sys.argv[1].lower()
        
        if test_type == 'full':
            test_full_pipeline()
        elif test_type == 'preprocess':
            test_preprocessing()
        elif test_type == 'sentiment':
            test_sentiment_analysis()
        elif test_type == 'visual':
            test_visualization()
        else:
            print("\nUsage: python test_modules.py [test_type]")
            print("\nAvailable test types:")
            print("  full       - Run complete analysis pipeline")
            print("  preprocess - Test preprocessing functions")
            print("  sentiment  - Test sentiment analysis")
            print("  visual     - Test visualization")
    else:
        # Run full pipeline by default
        test_full_pipeline()
