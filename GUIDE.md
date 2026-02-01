# Letterboxd Review Analytics - Complete Guide

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Project Overview](#project-overview)
3. [Module Documentation](#module-documentation)
4. [How It Works](#how-it-works)
5. [Customization](#customization)
6. [Troubleshooting](#troubleshooting)

---

## Quick Start

### Windows (PowerShell/CMD)

```bash
# Navigate to project
cd e:\letterboxd-review-analyser

# Create & activate virtual environment
python -m venv .venv
.\.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

### Mac/Linux

```bash
cd ~/letterboxd-review-analyser

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

python app.py
```

Then open **http://localhost:5000** in your browser.

---

## Project Overview

### What This App Does

1. **Scrapes Letterboxd** - Collects movie reviews with ratings and text
2. **Cleans Data** - Removes noise, normalizes text, calculates metrics
3. **Analyzes Sentiment** - Uses NLTK VADER to determine positive/negative sentiment
4. **Visualizes Results** - Generates charts and statistics
5. **Displays Results** - Shows comprehensive analysis on web interface

### Architecture

```
┌─────────────┐
│   User      │
│  (Browser)  │
└──────┬──────┘
       │ HTTP
       ▼
┌─────────────────────────────┐
│  Flask Web Application      │
│  (app.py)                   │
└──────┬──────────────────────┘
       │
       ├─► scraper.py ────► Letterboxd Website
       │
       ├─► preprocessor.py ─► data/reviews_clean.csv
       │
       ├─► analyzer.py ────► data/reviews_analyzed.csv
       │
       └─► visualizer.py ──► plots/sentiment.png
```

---

## Module Documentation

### 1. scraper.py - Web Scraping

**Purpose:** Fetch reviews from Letterboxd

**Key Functions:**

#### `scrape_letterboxd_reviews(movie_name, max_reviews=50)`
```python
reviews = scrape_letterboxd_reviews("The Matrix", max_reviews=100)
# Returns: List of dictionaries with review data
```

**Output Structure:**
```python
{
    'reviewer': 'user123',
    'rating': '★★★★★',
    'review_text': 'Amazing movie!',
    'date': '2024-01-15',
    'movie_name': 'The Matrix'
}
```

#### `save_reviews_to_csv(reviews, filepath)`
```python
save_reviews_to_csv(reviews, 'data/reviews.csv')
# Saves reviews to CSV file
```

#### `get_sample_reviews(movie_name)`
```python
sample = get_sample_reviews("Inception")
# Returns sample data for testing (fallback when scraping unavailable)
```

**Note:** The scraper includes a fallback to sample data if the live scraping fails. To enable real scraping on a live Letterboxd instance, you would need to enhance the URL parsing and CSS selectors based on Letterboxd's current HTML structure.

---

### 2. preprocessor.py - Data Cleaning

**Purpose:** Clean and prepare review text for analysis

**Key Functions:**

#### `clean_text(text)`
```python
raw = "Check https://example.com! #amazing :)"
clean = clean_text(raw)
# Returns: "check amazing"

# Removes:
# - URLs
# - Email addresses
# - Special characters (keeps letters, numbers, spaces, punctuation)
# - Extra whitespace
# - Converts to lowercase
```

#### `remove_empty_reviews(df)`
```python
df_cleaned = remove_empty_reviews(df)
# Removes rows with NaN or empty review_text
```

#### `count_words(text)`
```python
count = count_words("This is a test")
# Returns: 4
```

#### `preprocess_reviews(input_filepath, output_filepath)`
**Main preprocessing pipeline**
```python
df_clean = preprocess_reviews(
    'data/reviews_raw.csv',
    'data/reviews_clean.csv'
)
# Performs complete preprocessing and returns DataFrame
```

**Processing Steps:**
1. Load raw data
2. Remove empty reviews
3. Clean all text
4. Remove reviews that become empty after cleaning
5. Calculate word counts
6. Reorder columns
7. Save to CSV

---

### 3. analyzer.py - Sentiment Analysis

**Purpose:** Analyze sentiment using NLTK VADER

**Key Functions:**

#### `initialize_sentiment_analyzer()`
```python
analyzer = initialize_sentiment_analyzer()
# Returns initialized SentimentIntensityAnalyzer
```

#### `analyze_sentiment(text, analyzer)`
```python
score = analyze_sentiment("This movie is amazing!", analyzer)
# Returns: 0.752 (between -1 and 1)
```

**Sentiment Score Interpretation:**
- **1.0 to 0.05**: Positive
- **0.05 to -0.05**: Neutral
- **-0.05 to -1.0**: Negative

#### `analyze_all_reviews(df)`
**Analyzes all reviews in DataFrame**
```python
df_analyzed = analyze_all_reviews(df_clean)
# Adds columns: sentiment_score, sentiment_class
```

**Output Columns:**
```python
# Original columns + new ones:
sentiment_score  # float: -1 to 1
sentiment_class  # string: 'positive', 'neutral', 'negative'
```

#### `calculate_sentiment_stats(df)`
```python
stats = calculate_sentiment_stats(df_analyzed)
# Returns dictionary with comprehensive statistics

# Example output:
{
    'total_reviews': 50,
    'positive_reviews': 35,
    'negative_reviews': 5,
    'neutral_reviews': 10,
    'positive_pct': 70.0,
    'negative_pct': 10.0,
    'neutral_pct': 20.0,
    'avg_sentiment': 0.752,
    'max_sentiment': 0.996,
    'min_sentiment': -0.905
}
```

#### `get_sentiment_distribution(df)`
```python
dist = get_sentiment_distribution(df_analyzed)
# Returns: {'positive': 35, 'neutral': 10, 'negative': 5}
```

---

### 4. visualizer.py - Visualization

**Purpose:** Create charts and visualizations

**Key Functions:**

#### `create_sentiment_chart(sentiment_distribution, movie_name, output_path)`
```python
create_sentiment_chart(
    {'positive': 35, 'neutral': 10, 'negative': 5},
    'The Matrix',
    'plots/matrix_sentiment.png'
)
# Creates bar chart and saves to file
```

**Chart Features:**
- Color-coded bars (green=positive, gray=neutral, red=negative)
- Value labels on bars
- Grid for readability
- Professional styling

#### `create_sentiment_score_distribution(df, movie_name, output_path)`
```python
create_sentiment_score_distribution(
    df_analyzed,
    'Inception',
    'plots/inception_scores.png'
)
# Creates histogram of sentiment scores
```

#### `create_combined_report(sentiment_distribution, avg_sentiment, movie_name, output_path)`
```python
create_combined_report(
    {'positive': 35, 'neutral': 10, 'negative': 5},
    0.752,
    'The Shawshank Redemption',
    'plots/report.png'
)
# Creates comprehensive report visualization
```

---

### 5. app.py - Flask Web Application

**Purpose:** Web server and routing

**Key Routes:**

#### `GET /`
- Serves home page (index.html)
- Contains search form

#### `POST /api/analyze`
- Receives: `{"movie_name": "Inception"}`
- Executes full analysis pipeline
- Returns: JSON with analysis results

#### `GET /results`
- Serves results page (results.html)

#### `GET /plots/<filename>`
- Serves generated chart images

#### `GET /api/health`
- Health check endpoint

**Processing Flow in `/api/analyze`:**
```
1. Validate input
2. Scrape reviews ────→ data/reviews_raw.csv
3. Preprocess ────────→ data/reviews_clean.csv
4. Analyze sentiment ─→ data/reviews_analyzed.csv
5. Create chart ──────→ plots/sentiment.png
6. Return JSON response
```

---

## How It Works

### Step-by-Step Process

#### 1️⃣ Data Collection
- User enters movie name
- App queries Letterboxd (or uses sample data)
- Reviews extracted: text, rating, date, reviewer

**Output:** `data/reviews_raw.csv`
```
movie_name,reviewer,rating,review_text,date
Inception,user1,★★★★★,"Mind-bending masterpiece!",2024-01-15
```

#### 2️⃣ Data Cleaning
- Remove empty reviews
- Convert text to lowercase
- Remove URLs, special characters
- Calculate word counts

**Output:** `data/reviews_clean.csv`
```
movie_name,reviewer,rating,review_text,word_count,date
Inception,user1,★★★★★,"mind bending masterpiece",3,2024-01-15
```

#### 3️⃣ Sentiment Analysis
- VADER analyzes each review
- Assigns sentiment score (-1 to 1)
- Classifies as positive/neutral/negative

**Output:** `data/reviews_analyzed.csv`
```
...,sentiment_score,sentiment_class
...,0.892,positive
```

#### 4️⃣ Statistical Analysis
- Count positive/neutral/negative
- Calculate average sentiment
- Determine percentages

**Output:**
```python
{
    'total_reviews': 50,
    'avg_sentiment': 0.752,
    'positive_reviews': 35,
    'positive_pct': 70.0
}
```

#### 5️⃣ Visualization
- Create bar chart of sentiment distribution
- Add labels and styling
- Save as PNG

**Output:** `plots/Inception_sentiment.png`

#### 6️⃣ Display Results
- Show statistics on web page
- Display chart
- List sample reviews
- Show detailed metrics

---

## Sentiment Analysis Deep Dive

### What is VADER?

**VADER (Valence Aware Dictionary and sEntiment Reasoner)**
- Lexicon-based sentiment analysis tool
- Optimized for social media and reviews
- Understands emoticons, slang, capital letters
- Returns probability of positive/negative/neutral

### How VADER Works

1. **Tokenizes** the text into words
2. **Looks up** each word in VADER lexicon
3. **Applies rules** for intensifiers, negations
4. **Calculates** compound score

### Example

```
Text: "This movie is absolutely amazing!"

Step 1: Split into words
["This", "movie", "is", "absolutely", "amazing"]

Step 2: Look up sentiment values
"amazing" = 0.646
"absolutely" = 0.293 (intensifier)

Step 3: Combine and normalize
Final compound score = 0.8 (positive)
```

### Threshold Interpretation

| Score | Classification | Example |
|-------|-----------------|---------|
| 0.7-1.0 | Strong Positive | "Absolutely brilliant!" |
| 0.05-0.7 | Positive | "Really good movie" |
| -0.05-0.05 | Neutral | "It was okay" |
| -0.7 to -0.05 | Negative | "Pretty bad" |
| -1.0 to -0.7 | Strong Negative | "Absolutely terrible!" |

---

## Customization

### Change Sentiment Thresholds

In `analyzer.py`, modify `analyze_all_reviews()`:

```python
def classify_sentiment(score):
    if score > 0.1:      # Changed from 0.05
        return 'positive'
    elif score < -0.1:   # Changed from -0.05
        return 'negative'
    else:
        return 'neutral'
```

### Change Chart Colors

In `visualizer.py`, modify `create_sentiment_chart()`:

```python
colors = {
    'positive': '#FF6B6B',   # Change to your color
    'neutral': '#4ECDC4',
    'negative': '#95E1D3'
}
```

### Change Maximum Reviews

In `app.py`:

```python
reviews = scrape_letterboxd_reviews(movie_name, max_reviews=100)  # Changed from 50
```

### Change Port

In `app.py`:

```python
if __name__ == '__main__':
    app.run(debug=True, port=8080)  # Changed from 5000
```

### Add Database Storage

Replace CSV storage with SQLite:

```python
import sqlite3

def save_reviews_to_db(reviews):
    conn = sqlite3.connect('reviews.db')
    cursor = conn.cursor()
    
    for review in reviews:
        cursor.execute('''
            INSERT INTO reviews (movie_name, reviewer, rating, review_text)
            VALUES (?, ?, ?, ?)
        ''', (review['movie_name'], review['reviewer'], 
              review['rating'], review['review_text']))
    
    conn.commit()
    conn.close()
```

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'flask'"

**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: Port 5000 already in use

**Solution:** Change port in `app.py`
```python
app.run(port=5001)
```

Or kill the process using the port:
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti :5000 | xargs kill -9
```

### Issue: NLTK VADER lexicon not found

**Solution:** Manually download
```python
import nltk
nltk.download('vader_lexicon')
```

### Issue: No reviews found for movie

**Solution:** Try different movie name or use sample data by setting in `config.py`:
```python
USE_SAMPLE_DATA = True
```

### Issue: Chart not displaying

**Solution:** Check that matplotlib is installed
```bash
pip install --upgrade matplotlib
```

### Issue: Virtual environment activation fails

**Solution:** Recreate virtual environment
```bash
# Remove old venv
rm -r .venv  # or rmdir /s .venv on Windows

# Create new one
python -m venv .venv

# Activate
.\.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

---

## Testing

### Run Unit Tests

```bash
# Test full pipeline
python test_modules.py full

# Test preprocessing only
python test_modules.py preprocess

# Test sentiment analysis
python test_modules.py sentiment

# Test visualization
python test_modules.py visual
```

### Manual Testing

```python
# Open Python interactive shell
python

>>> from scraper import get_sample_reviews
>>> reviews = get_sample_reviews("Test Movie")
>>> print(reviews[0])

>>> from preprocessor import clean_text
>>> clean = clean_text("Hello! This is a TEST #movie :)")
>>> print(clean)

>>> from analyzer import initialize_sentiment_analyzer, analyze_sentiment
>>> analyzer = initialize_sentiment_analyzer()
>>> score = analyze_sentiment("This movie is amazing!", analyzer)
>>> print(score)
```

---

## Performance Tips

### 1. Cache Results
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def analyze_sentiment(text):
    # Cached results
    pass
```

### 2. Batch Processing
```python
# Instead of analyzing one at a time
df['sentiment'] = df['review_text'].apply(analyze)

# Much faster!
```

### 3. Limit Reviews
```python
# Start with fewer reviews for testing
reviews = scrape_letterboxd_reviews(movie, max_reviews=20)
```

### 4. Use Threading
```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=4) as executor:
    results = executor.map(analyze_sentiment, reviews)
```

---

## Next Steps

1. **Enhance Scraping:** Improve Letterboxd HTML parsing
2. **Add Database:** Store results in SQLite/PostgreSQL
3. **User Accounts:** Allow users to save analyses
4. **Comparisons:** Compare sentiment across multiple movies
5. **Export:** Generate PDF reports
6. **APIs:** Create REST API for third-party access
7. **ML Models:** Use more advanced NLP models
8. **Real-time:** WebSocket for live updates

---

**Enjoy analyzing movie reviews! 🍿📊**
