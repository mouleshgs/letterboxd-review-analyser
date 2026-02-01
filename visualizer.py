"""
Visualization module for creating charts and graphs.
Generates sentiment distribution visualizations.
"""

import matplotlib.pyplot as plt
import matplotlib
import os

# Use non-interactive backend for better compatibility
matplotlib.use('Agg')


def create_sentiment_chart(sentiment_distribution, movie_name, output_path):
    """
    Creates and saves a sentiment distribution bar chart.
    
    Args:
        sentiment_distribution (dict): Dictionary with sentiment counts
        movie_name (str): Name of the movie
        output_path (str): Path to save the chart image
    
    Returns:
        bool: True if successful, False otherwise
    """
    
    try:
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Extract sentiment data
        labels = list(sentiment_distribution.keys())
        values = list(sentiment_distribution.values())
        
        # Define colors for each sentiment
        colors = {
            'positive': '#2ecc71',   # Green
            'neutral': '#95a5a6',    # Gray
            'negative': '#e74c3c'    # Red
        }
        bar_colors = [colors.get(label, '#3498db') for label in labels]
        
        # Create figure
        plt.figure(figsize=(10, 6))
        
        # Create bar chart
        bars = plt.bar(labels, values, color=bar_colors, edgecolor='black', linewidth=1.5)
        
        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontsize=12, fontweight='bold')
        
        # Customize chart
        plt.title(f'Sentiment Distribution - {movie_name}', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Sentiment', fontsize=12, fontweight='bold')
        plt.ylabel('Number of Reviews', fontsize=12, fontweight='bold')
        plt.ylim(0, max(values) * 1.15 if max(values) > 0 else 10)
        
        # Add grid for better readability
        plt.grid(axis='y', alpha=0.3, linestyle='--')
        
        # Adjust layout to prevent label cutoff
        plt.tight_layout()
        
        # Save figure
        plt.savefig(output_path, dpi=100, bbox_inches='tight')
        print(f"✓ Sentiment chart saved to {output_path}")
        
        # Close the figure to free memory
        plt.close()
        
        return True
        
    except Exception as e:
        print(f"✗ Error creating chart: {str(e)}")
        return False


def create_sentiment_score_distribution(df, movie_name, output_path):
    """
    Creates and saves a histogram of sentiment scores.
    
    Args:
        df (DataFrame): Dataframe with sentiment_score column
        movie_name (str): Name of the movie
        output_path (str): Path to save the chart image
    
    Returns:
        bool: True if successful, False otherwise
    """
    
    try:
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Create figure
        plt.figure(figsize=(10, 6))
        
        # Create histogram
        plt.hist(df['sentiment_score'], bins=20, color='#3498db', edgecolor='black', alpha=0.7)
        
        # Add vertical line for average sentiment
        avg_sentiment = df['sentiment_score'].mean()
        plt.axvline(avg_sentiment, color='red', linestyle='--', linewidth=2, label=f'Average: {avg_sentiment:.3f}')
        
        # Customize chart
        plt.title(f'Sentiment Score Distribution - {movie_name}', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Sentiment Score', fontsize=12, fontweight='bold')
        plt.ylabel('Frequency', fontsize=12, fontweight='bold')
        plt.legend(fontsize=10)
        
        # Add grid for better readability
        plt.grid(axis='y', alpha=0.3, linestyle='--')
        
        # Adjust layout
        plt.tight_layout()
        
        # Save figure
        plt.savefig(output_path, dpi=100, bbox_inches='tight')
        print(f"✓ Score distribution chart saved to {output_path}")
        
        # Close the figure to free memory
        plt.close()
        
        return True
        
    except Exception as e:
        print(f"✗ Error creating score distribution chart: {str(e)}")
        return False


def create_combined_report(sentiment_distribution, avg_sentiment, movie_name, output_path):
    """
    Creates a combined report visualization with multiple charts.
    
    Args:
        sentiment_distribution (dict): Dictionary with sentiment counts
        avg_sentiment (float): Average sentiment score
        movie_name (str): Name of the movie
        output_path (str): Path to save the report image
    
    Returns:
        bool: True if successful, False otherwise
    """
    
    try:
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Create figure with subplots
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Prepare data
        labels = list(sentiment_distribution.keys())
        values = list(sentiment_distribution.values())
        
        # Define colors
        colors = {
            'positive': '#2ecc71',
            'neutral': '#95a5a6',
            'negative': '#e74c3c'
        }
        bar_colors = [colors.get(label, '#3498db') for label in labels]
        
        # Create bar chart
        bars = ax.bar(labels, values, color=bar_colors, edgecolor='black', linewidth=1.5)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontsize=12, fontweight='bold')
        
        # Customize
        ax.set_title(f'Sentiment Analysis Report - {movie_name}\nAverage Sentiment: {avg_sentiment:.3f}',
                    fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel('Sentiment', fontsize=11, fontweight='bold')
        ax.set_ylabel('Number of Reviews', fontsize=11, fontweight='bold')
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        
        # Adjust layout
        plt.tight_layout()
        
        # Save figure
        plt.savefig(output_path, dpi=100, bbox_inches='tight')
        print(f"✓ Combined report saved to {output_path}")
        
        # Close the figure
        plt.close()
        
        return True
        
    except Exception as e:
        print(f"✗ Error creating combined report: {str(e)}")
        return False
