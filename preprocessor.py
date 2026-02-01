"""
Data preprocessing module for cleaning and preparing reviews for analysis.
Handles text cleaning, normalization, and feature extraction.
"""

import pandas as pd
import re


def clean_text(text):
    """
    Cleans review text by removing URLs, special characters, and extra whitespace.
    
    Args:
        text (str): Raw review text
    
    Returns:
        str: Cleaned review text
    """
    
    if not isinstance(text, str):
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)
    
    # Remove special characters but keep spaces and basic punctuation
    text = re.sub(r'[^a-zA-Z0-9\s\.\!\?\,\:]', '', text)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text


def remove_empty_reviews(df):
    """
    Removes reviews with empty or NaN text content.
    
    Args:
        df (DataFrame): Input dataframe with reviews
    
    Returns:
        DataFrame: Dataframe with empty reviews removed
    """
    
    # Remove rows where review_text is empty or NaN
    df = df[df['review_text'].notna()]
    df = df[df['review_text'].str.strip() != '']
    
    print(f"✓ Removed empty reviews. Remaining: {len(df)} reviews")
    return df


def count_words(text):
    """
    Counts the number of words in a text.
    
    Args:
        text (str): Text to count words in
    
    Returns:
        int: Number of words
    """
    
    if not isinstance(text, str):
        return 0
    
    return len(text.split())


def preprocess_reviews(input_filepath, output_filepath):
    """
    Main preprocessing function that cleans and prepares reviews.
    
    Args:
        input_filepath (str): Path to raw reviews CSV
        output_filepath (str): Path to save cleaned reviews CSV
    
    Returns:
        DataFrame: Processed dataframe or None if error occurs
    """
    
    try:
        # Read raw reviews
        print("📂 Reading raw reviews...")
        df = pd.read_csv(input_filepath)
        print(f"✓ Loaded {len(df)} reviews")
        
        # Remove empty reviews
        df = remove_empty_reviews(df)
        
        # Clean review text
        print("🧹 Cleaning review text...")
        df['review_text'] = df['review_text'].apply(clean_text)
        
        # Remove reviews that became empty after cleaning
        df = df[df['review_text'].str.strip() != '']
        
        # Add word count column
        print("📊 Calculating word counts...")
        df['word_count'] = df['review_text'].apply(count_words)
        
        # Reorder columns
        if 'date' in df.columns:
            df = df[['movie_name', 'reviewer', 'rating', 'review_text', 'word_count', 'date']]
        else:
            df = df[['movie_name', 'reviewer', 'rating', 'review_text', 'word_count']]
        
        # Save cleaned reviews
        df.to_csv(output_filepath, index=False, encoding='utf-8')
        print(f"✓ Cleaned reviews saved to {output_filepath}")
        print(f"✓ Final count: {len(df)} reviews after cleaning")
        
        return df
        
    except FileNotFoundError:
        print(f"✗ File not found: {input_filepath}")
        return None
    except Exception as e:
        print(f"✗ Error during preprocessing: {str(e)}")
        return None


def get_preprocessing_stats(df):
    """
    Calculates and returns statistics about the preprocessed data.
    
    Args:
        df (DataFrame): Preprocessed reviews dataframe
    
    Returns:
        dict: Dictionary containing preprocessing statistics
    """
    
    if df is None or len(df) == 0:
        return {}
    
    stats = {
        'total_reviews': len(df),
        'avg_word_count': df['word_count'].mean(),
        'min_word_count': df['word_count'].min(),
        'max_word_count': df['word_count'].max(),
        'total_words': df['word_count'].sum()
    }
    
    return stats
