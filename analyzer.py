"""
Sentiment analysis module using NLTK VADER.
Analyzes sentiment polarity and generates statistics.
"""

import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk


# Download required NLTK data
try:
    nltk.data.find('sentiment/vader_lexicon')
except LookupError:
    print("📥 Downloading NLTK VADER lexicon...")
    nltk.download('vader_lexicon', quiet=True)


def initialize_sentiment_analyzer():
    """
    Initializes the NLTK VADER sentiment analyzer.
    
    Returns:
        SentimentIntensityAnalyzer: Initialized analyzer
    """
    
    return SentimentIntensityAnalyzer()


def analyze_sentiment(text, analyzer):
    """
    Analyzes sentiment of a single review using VADER.
    
    Args:
        text (str): Review text to analyze
        analyzer (SentimentIntensityAnalyzer): Sentiment analyzer
    
    Returns:
        float: Compound sentiment score between -1 (negative) and 1 (positive)
    """
    
    if not isinstance(text, str) or len(text.strip()) == 0:
        return 0.0
    
    # Get sentiment scores
    scores = analyzer.polarity_scores(text)
    
    # Return compound score
    return scores['compound']


def analyze_all_reviews(df):
    """
    Performs sentiment analysis on all reviews in the dataframe.
    
    Args:
        df (DataFrame): Dataframe with review_text column
    
    Returns:
        DataFrame: Dataframe with added sentiment columns
    """
    
    print("🔍 Analyzing sentiment...")
    
    # Initialize analyzer
    analyzer = initialize_sentiment_analyzer()
    
    # Apply sentiment analysis to each review
    df['sentiment_score'] = df['review_text'].apply(lambda x: analyze_sentiment(x, analyzer))
    
    # Classify sentiment as positive, neutral, or negative
    def classify_sentiment(score):
        if score > 0.05:
            return 'positive'
        elif score < -0.05:
            return 'negative'
        else:
            return 'neutral'
    
    df['sentiment_class'] = df['sentiment_score'].apply(classify_sentiment)
    
    print("✓ Sentiment analysis complete")
    return df


def calculate_sentiment_stats(df):
    """
    Calculates sentiment statistics from analyzed reviews.
    
    Args:
        df (DataFrame): Dataframe with sentiment_score and sentiment_class columns
    
    Returns:
        dict: Dictionary containing sentiment statistics
    """
    
    if df is None or len(df) == 0:
        return {}
    
    # Count reviews by sentiment class
    sentiment_counts = df['sentiment_class'].value_counts().to_dict()
    
    # Calculate percentages
    total_reviews = len(df)
    positive_pct = (sentiment_counts.get('positive', 0) / total_reviews * 100) if total_reviews > 0 else 0
    negative_pct = (sentiment_counts.get('negative', 0) / total_reviews * 100) if total_reviews > 0 else 0
    neutral_pct = (sentiment_counts.get('neutral', 0) / total_reviews * 100) if total_reviews > 0 else 0
    
    # Calculate average sentiment
    avg_sentiment = df['sentiment_score'].mean()
    
    stats = {
        'total_reviews': total_reviews,
        'positive_reviews': sentiment_counts.get('positive', 0),
        'negative_reviews': sentiment_counts.get('negative', 0),
        'neutral_reviews': sentiment_counts.get('neutral', 0),
        'positive_pct': round(positive_pct, 2),
        'negative_pct': round(negative_pct, 2),
        'neutral_pct': round(neutral_pct, 2),
        'avg_sentiment': round(avg_sentiment, 3),
        'max_sentiment': round(df['sentiment_score'].max(), 3),
        'min_sentiment': round(df['sentiment_score'].min(), 3)
    }
    
    return stats


def get_sentiment_distribution(df):
    """
    Gets the distribution of sentiment classes for visualization.
    
    Args:
        df (DataFrame): Dataframe with sentiment_class column
    
    Returns:
        dict: Dictionary with sentiment class counts
    """
    
    if df is None or len(df) == 0:
        return {'positive': 0, 'neutral': 0, 'negative': 0}
    
    distribution = df['sentiment_class'].value_counts().to_dict()
    
    # Ensure all categories are present
    return {
        'positive': distribution.get('positive', 0),
        'neutral': distribution.get('neutral', 0),
        'negative': distribution.get('negative', 0)
    }


def save_analyzed_reviews(df, filepath):
    """
    Saves reviews with sentiment analysis to CSV.
    
    Args:
        df (DataFrame): Dataframe with sentiment analysis
        filepath (str): Path to save the file
    
    Returns:
        bool: True if successful, False otherwise
    """
    
    try:
        df.to_csv(filepath, index=False, encoding='utf-8')
        print(f"✓ Analyzed reviews saved to {filepath}")
        return True
    except Exception as e:
        print(f"✗ Error saving analyzed reviews: {str(e)}")
        return False
