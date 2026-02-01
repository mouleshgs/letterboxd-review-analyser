# Configuration file for Letterboxd Review Analytics

# Application Settings
DEBUG = True
TESTING = False
SECRET_KEY = 'your-secret-key-here-change-in-production'

# Flask Configuration
FLASK_ENV = 'development'
FLASK_DEBUG = True

# Data Paths
DATA_DIR = 'data'
PLOTS_DIR = 'plots'
TEMPLATES_DIR = 'templates'
STATIC_DIR = 'static'

# Scraping Settings
MAX_REVIEWS = 50
REQUEST_TIMEOUT = 10
RETRY_ATTEMPTS = 3

# Analysis Settings
SENTIMENT_POSITIVE_THRESHOLD = 0.05
SENTIMENT_NEGATIVE_THRESHOLD = -0.05

# Visualization Settings
CHART_DPI = 100
CHART_FORMAT = 'png'
CHART_FIGSIZE = (10, 6)

# File Names
RAW_REVIEWS_FILE = 'reviews_raw.csv'
CLEAN_REVIEWS_FILE = 'reviews_clean.csv'
ANALYZED_REVIEWS_FILE = 'reviews_analyzed.csv'

# Feature Flags
USE_SAMPLE_DATA = True  # Set to False to use real Letterboxd scraping
SAVE_CHARTS = True
SAVE_DATA = True
