# 🎬 Letterboxd Review Analytics

A simple, full-stack web application that analyzes movie reviews from Letterboxd using sentiment analysis and data visualization.

## Features

✨ **Core Features:**
- 🔍 Scrape reviews from Letterboxd
- 🧹 Clean and preprocess review text
- 💭 Sentiment analysis using NLTK VADER
- 📊 Beautiful sentiment distribution charts
- 📈 Comprehensive analysis statistics
- 🎨 Clean and intuitive UI

## Tech Stack

**Backend:**
- Python Flask - Web framework
- requests - HTTP requests
- BeautifulSoup4 - Web scraping
- pandas - Data manipulation
- NLTK - Natural Language Processing
- matplotlib - Data visualization

**Frontend:**
- HTML5
- CSS3 (with modern design)
- JavaScript (vanilla)

## Project Structure

```
letterboxd-review-analyser/
├── app.py                 # Flask application & routes
├── scraper.py            # Web scraping module
├── preprocessor.py       # Data cleaning & preprocessing
├── analyzer.py           # Sentiment analysis module
├── visualizer.py         # Chart generation module
├── requirements.txt      # Python dependencies
├── data/                 # Data storage
│   ├── reviews_raw.csv
│   ├── reviews_clean.csv
│   └── reviews_analyzed.csv
├── plots/                # Generated visualizations
│   └── sentiment.png
├── templates/            # HTML templates
│   ├── index.html
│   └── results.html
└── static/               # Static files
    ├── style.css
    ├── script.js
    └── results.js
```

## Installation

### Step 1: Clone/Download the Project
```bash
cd e:\letterboxd-review-analyser
```

### Step 2: Create Virtual Environment
```bash
python -m venv .venv
```

### Step 3: Activate Virtual Environment

**Windows (PowerShell):**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
.\.venv\Scripts\activate.bat
```

**Mac/Linux:**
```bash
source .venv/bin/activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Run the Application
```bash
python app.py
```

The application will start at: **http://localhost:5000**

## Usage

### 1. Home Page
- Enter a movie name in the search box
- Click "Analyze Reviews" button
- Wait for the analysis to complete

### 2. How the Analysis Works

**Step 1: Scraping**
- Fetches reviews from Letterboxd
- Extracts review text, ratings, and dates
- Saves raw data to `data/reviews_raw.csv`

**Step 2: Preprocessing**
- Removes empty reviews
- Converts text to lowercase
- Removes URLs and special characters
- Calculates word count
- Saves cleaned data to `data/reviews_clean.csv`

**Step 3: Sentiment Analysis**
- Uses NLTK VADER sentiment analyzer
- Assigns sentiment scores (-1 to 1)
- Classifies as positive/neutral/negative
- Saves analyzed data to `data/reviews_analyzed.csv`

**Step 4: Visualization**
- Generates sentiment distribution bar chart
- Creates statistics summary
- Displays results on results page

### 3. Results Page
View comprehensive analysis including:
- Total number of reviews analyzed
- Average sentiment score
- Count of positive, neutral, and negative reviews
- Sentiment distribution chart
- Sample reviews with sentiment scores
- Statistical details

## Code Modules Explained

### `app.py` - Flask Application
Main application file containing:
- Flask routes for home and results pages
- `/api/analyze` endpoint for processing
- Error handling
- File serving

### `scraper.py` - Web Scraping
Functions to:
- Scrape Letterboxd for reviews
- Extract review data
- Save to CSV
- Fall back to sample data

### `preprocessor.py` - Data Cleaning
Functions to:
- Clean review text
- Remove empty reviews
- Calculate word counts
- Prepare data for analysis

### `analyzer.py` - Sentiment Analysis
Functions to:
- Initialize VADER sentiment analyzer
- Analyze individual reviews
- Calculate sentiment statistics
- Generate sentiment distribution

### `visualizer.py` - Visualization
Functions to:
- Create sentiment distribution charts
- Generate score histograms
- Create combined reports
- Save plots as images

## API Endpoints

### `GET /`
Returns the home page

### `POST /api/analyze`
**Request:**
```json
{
  "movie_name": "The Shawshank Redemption"
}
```

**Response:**
```json
{
  "success": true,
  "movie_name": "The Shawshank Redemption",
  "timestamp": "2024-01-15 10:30:45",
  "stats": {
    "total_reviews": 50,
    "average_sentiment": 0.752,
    "positive_reviews": 35,
    "negative_reviews": 5,
    "neutral_reviews": 10,
    "positive_pct": 70.0,
    "negative_pct": 10.0,
    "neutral_pct": 20.0,
    "max_sentiment": 0.996,
    "min_sentiment": -0.905
  },
  "sentiment_distribution": {
    "positive": 35,
    "neutral": 10,
    "negative": 5
  },
  "chart_url": "/plots/The_Shawshank_Redemption_sentiment.png",
  "sample_reviews": [...]
}
```

### `GET /api/health`
Health check endpoint

## Data Files

### reviews_raw.csv
```
movie_name,reviewer,rating,review_text,date
The Matrix,user1,★★★★★,"Amazing sci-fi film!",2024-01-15
```

### reviews_clean.csv
```
movie_name,reviewer,rating,review_text,word_count,date
The Matrix,user1,★★★★★,"amazing sci fi film",4,2024-01-15
```

### reviews_analyzed.csv
```
movie_name,reviewer,rating,review_text,word_count,date,sentiment_score,sentiment_class
The Matrix,user1,★★★★★,"amazing sci fi film",4,2024-01-15,0.752,positive
```

## Sentiment Analysis Explained

The application uses **NLTK VADER (Valence Aware Dictionary and sEntiment Reasoner)**, a lexicon and rule-based sentiment analysis tool optimized for social media and review text.

**Sentiment Score Range:** -1.0 to 1.0
- **1.0**: Most positive
- **0.0**: Neutral
- **-1.0**: Most negative

**Classification:**
- **Positive**: score > 0.05
- **Neutral**: -0.05 ≤ score ≤ 0.05
- **Negative**: score < -0.05

## Troubleshooting

### Port Already in Use
If port 5000 is already in use, modify in `app.py`:
```python
app.run(debug=True, port=5001)  # Use different port
```

### NLTK Data Missing
The app automatically downloads required NLTK data on first run. If issues persist:
```python
import nltk
nltk.download('vader_lexicon')
```

### Virtual Environment Issues
Re-create the virtual environment:
```bash
rm -r .venv  # or rmdir /s .venv on Windows
python -m venv .venv
```

## Features & Best Practices

✅ **Modular Design**
- Separate modules for each functionality
- Easy to test and maintain
- Clear separation of concerns

✅ **Error Handling**
- Try-catch blocks for robustness
- User-friendly error messages
- Graceful fallbacks

✅ **Code Comments**
- Comprehensive docstrings
- Clear inline comments
- Easy to understand

✅ **UI/UX**
- Responsive design
- Modern, clean interface
- Intuitive navigation
- Loading states and feedback

## Future Enhancements

📌 **Planned Features:**
- Direct Letterboxd API integration
- User authentication
- Search history
- Multiple movie comparisons
- Export results as PDF
- Advanced NLP models
- Real-time scraping updates
- Database storage (SQLite/PostgreSQL)

## License

This project is open source and available for educational purposes.

## Contact & Support

For issues, questions, or contributions, please feel free to reach out!

---

**Built with ❤️ using Flask, NLTK, and Python**
