"""
Web scraper module for Letterboxd reviews.
Extracts review text, ratings, and dates from Letterboxd movie pages.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
import csv


def scrape_letterboxd_reviews(movie_name, max_reviews=50):
    """
    Scrapes reviews from Letterboxd for a given movie.
    
    Args:
        movie_name (str): Name of the movie to search for
        max_reviews (int): Maximum number of reviews to scrape (default: 50)
    
    Returns:
        list: List of dictionaries containing review data
    """
    
    # Convert movie name to Letterboxd URL format (lowercase, hyphens instead of spaces)
    movie_slug = movie_name.lower().replace(" ", "-")
    url = f"https://letterboxd.com/search/{movie_name}/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    reviews = []
    
    try:
        # Try to fetch the search page
        print(f"🔍 Searching for '{movie_name}' on Letterboxd...")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all reviews on the page
        review_items = soup.find_all('div', class_='review')
        
        print(f"✓ Found {len(review_items)} reviews")
        
        for review_item in review_items[:max_reviews]:
            try:
                # Extract review text
                review_text_elem = review_item.find('p', class_='review-text')
                review_text = review_text_elem.text.strip() if review_text_elem else ""
                
                # Extract rating (Letterboxd uses star ratings)
                rating_elem = review_item.find('span', class_='rating')
                rating = rating_elem.text.strip() if rating_elem else "N/A"
                
                # Extract review date
                date_elem = review_item.find('time')
                review_date = date_elem.get('datetime', datetime.now().isoformat()) if date_elem else datetime.now().isoformat()
                
                # Extract reviewer name
                reviewer_elem = review_item.find('a', class_='reviewer')
                reviewer = reviewer_elem.text.strip() if reviewer_elem else "Anonymous"
                
                # Add to reviews list if review text is not empty
                if review_text:
                    reviews.append({
                        'reviewer': reviewer,
                        'rating': rating,
                        'review_text': review_text,
                        'date': review_date,
                        'movie_name': movie_name
                    })
                    
            except Exception as e:
                print(f"⚠ Error parsing review: {str(e)}")
                continue
        
        print(f"✓ Successfully scraped {len(reviews)} reviews")
        return reviews
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Network error while scraping: {str(e)}")
        return []
    except Exception as e:
        print(f"✗ Error during scraping: {str(e)}")
        return []


def save_reviews_to_csv(reviews, filepath):
    """
    Saves scraped reviews to a CSV file.
    
    Args:
        reviews (list): List of review dictionaries
        filepath (str): Path to save the CSV file
    
    Returns:
        bool: True if successful, False otherwise
    """
    
    if not reviews:
        print("⚠ No reviews to save")
        return False
    
    try:
        # Create DataFrame from reviews
        df = pd.DataFrame(reviews)
        
        # Save to CSV
        df.to_csv(filepath, index=False, encoding='utf-8')
        print(f"✓ Reviews saved to {filepath}")
        return True
        
    except Exception as e:
        print(f"✗ Error saving reviews: {str(e)}")
        return False


def get_sample_reviews(movie_name):
    """
    Returns sample reviews for demonstration purposes.
    Reviews are generated differently for each movie based on a hash of the movie name.
    
    Args:
        movie_name (str): Name of the movie
    
    Returns:
        list: List of sample review dictionaries with varied sentiment per movie
    """
    import random
    
    # Use movie name to seed random for consistent but different results per movie
    random.seed(hash(movie_name.lower()) % (2**32))
    
    # Review templates with different sentiments
    positive_reviews = [
        'Absolutely brilliant and memorable. One of the best films ever made!',
        'Masterpiece! Every scene is perfectly crafted. A true work of art.',
        'Incredible storytelling and outstanding performances throughout. Highly recommended!',
        'This film exceeded my expectations. Absolutely phenomenal in every way.',
        'Stunning cinematography and brilliant direction. A must-watch!',
        'Excellent film with compelling narrative and great character development.',
        'Really enjoyed this. Great entertainment value and emotional depth.',
        'Outstanding performances and impressive production value. Very impressed!',
        'Highly engaging from start to finish. Would definitely watch again.',
        'Great film with excellent pacing and interesting plot twists.',
        'Well-crafted with excellent acting and a captivating story.',
        'Simply wonderful! Loved every minute of it.',
        'Best film I\'ve seen in a long time. Absolutely fantastic.',
        'Brilliant work! Director nailed every aspect of this film.',
        'Amazing visual effects combined with perfect storytelling.',
    ]
    
    neutral_reviews = [
        'Good movie with solid performances and decent storyline. Worth watching.',
        'Entertaining film with some interesting moments and good direction.',
        'Solid movie with good acting and an engaging narrative overall.',
        'Pretty good film. Some great scenes mixed with a few slower moments.',
        'Enjoyed this one. Great visuals and decent character arcs throughout.',
        'It was okay. Some parts were really good but others felt slow.',
        'Average film. Not bad but nothing particularly special or memorable either.',
        'Mixed feelings. Good ideas but poor execution in several parts.',
        'Decent movie. Had its moments but also some predictable sections.',
        'Not perfect but entertaining enough for a casual watch.',
        'Interesting concept but could have been executed better.',
        'Watchable film with some notable scenes but overall inconsistent.',
        'Pretty entertaining. Not groundbreaking but worth your time.',
        'Good film that keeps you interested throughout most of it.',
        'Had potential and delivered reasonably well in most areas.',
    ]
    
    negative_reviews = [
        'Disappointed by this one. Started strong but lost momentum halfway through.',
        'Underwhelming. Had potential but failed to deliver on expectations.',
        'Quite disappointed with this film. Boring and predictable throughout.',
        'Waste of time. Poor plot and unconvincing characters made it hard to enjoy.',
        'Really bad film. Poorly paced and lacked any real substance or meaning.',
        'Terrible movie. Could not finish watching it. Very disappointed.',
        'Absolutely awful. One of the worst films I have ever seen.',
        'Did not enjoy this at all. Waste of valuable time.',
        'Disappointing on every level. Poor writing and weak characters.',
        'Painfully boring. Could not connect with any aspect of this film.',
        'Terrible execution of an already weak concept.',
        'Could not stand watching this. Turned it off halfway.',
        'Worst film I\'ve seen in recent memory. Terrible all around.',
        'Deeply flawed in every way. Do not recommend to anyone.',
        'Absolutely dreadful. Regret spending time on this movie.',
    ]
    
    # Create 40 reviews with varied sentiment (different distribution per movie)
    # This ensures different movies get different review distributions
    ratings_distribution = random.choices(
        [5, 4, 3, 2, 1],
        weights=[random.randint(15, 35), random.randint(15, 30), random.randint(15, 30), 
                 random.randint(5, 20), random.randint(5, 20)],
        k=40
    )
    
    reviews = []
    reviewer_names = [
        'alice_film', 'bob_critic', 'charlie_fan', 'diana_lover', 'evan_watcher',
        'fiona_buff', 'george_geek', 'hannah_enthusiast', 'ivan_admirer', 'julia_viewer',
        'kevin_pro', 'laura_movie', 'mike_cinema', 'nancy_screen', 'oscar_visual',
        'paul_story', 'quinn_direction', 'rachel_actor', 'sam_production', 'tina_award',
        'uriel_artistic', 'victor_dramatic', 'wendy_comedy', 'xavier_thriller', 'yara_adventure',
        'zack_scifi', 'amy_romance', 'brian_mystery', 'clara_horror', 'david_animation',
        'emma_indie', 'frank_blockbuster', 'gina_classic', 'henry_modern', 'iris_experimental',
        'jack_documentary', 'kate_series', 'liam_episode', 'mona_streaming', 'noah_digital'
    ]
    
    review_id = 0
    for i, rating in enumerate(ratings_distribution):
        if rating == 5:
            text = random.choice(positive_reviews)
            rating_str = '★★★★★'
        elif rating == 4:
            text = random.choice(positive_reviews if random.random() > 0.3 else neutral_reviews)
            rating_str = '★★★★'
        elif rating == 3:
            text = random.choice(neutral_reviews)
            rating_str = '★★★'
        elif rating == 2:
            text = random.choice(negative_reviews if random.random() > 0.3 else neutral_reviews)
            rating_str = '★★'
        else:  # rating == 1
            text = random.choice(negative_reviews)
            rating_str = '★'
        
        reviews.append({
            'reviewer': reviewer_names[i % len(reviewer_names)],
            'rating': rating_str,
            'review_text': text,
            'date': f'2024-{(i % 12) + 1:02d}-{(i % 28) + 1:02d}',
            'movie_name': movie_name
        })
        review_id += 1
    
    # Shuffle the reviews so they're not in sentiment order
    random.shuffle(reviews)
    return reviews
