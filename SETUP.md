# 🚀 Installation & Setup Guide

## Quick Setup (5 Minutes)

### Windows Users

```powershell
# 1. Navigate to project folder
cd e:\letterboxd-review-analyser

# 2. Run setup script (one-click installation)
.\setup.bat

# 3. After setup completes, run the app
python app.py

# 4. Open browser to http://localhost:5000
```

### Mac/Linux Users

```bash
# 1. Navigate to project folder
cd ~/letterboxd-review-analyser

# 2. Make setup script executable
chmod +x setup.sh

# 3. Run setup script
./setup.sh

# 4. Activate virtual environment
source .venv/bin/activate

# 5. Run the app
python app.py

# 6. Open browser to http://localhost:5000
```

---

## Manual Setup (Step by Step)

### Step 1: Install Python

**Windows:**
1. Download from https://www.python.org/downloads/
2. Run installer
3. ✅ Check "Add Python to PATH"
4. Click "Install Now"

**Mac:**
```bash
brew install python3
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install python3 python3-pip
```

### Step 2: Navigate to Project

```bash
# Windows
cd e:\letterboxd-review-analyser

# Mac/Linux
cd ~/letterboxd-review-analyser
```

### Step 3: Create Virtual Environment

```bash
# Windows, Mac, Linux (same command)
python -m venv .venv
```

### Step 4: Activate Virtual Environment

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

You should see `(.venv)` in your terminal prompt.

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Flask (web framework)
- requests (HTTP library)
- BeautifulSoup4 (web scraping)
- pandas (data processing)
- nltk (NLP/sentiment analysis)
- matplotlib (visualization)

### Step 6: Download NLTK Data

```bash
python -c "import nltk; nltk.download('vader_lexicon')"
```

This downloads the VADER sentiment lexicon (~2MB).

### Step 7: Run the Application

```bash
python app.py
```

**Expected Output:**
```
🚀 Starting Letterboxd Review Analytics...
📍 App running at http://localhost:5000
📝 Press CTRL+C to stop
```

### Step 8: Open in Browser

Navigate to: **http://localhost:5000**

You should see the home page! 🎉

---

## Verify Installation

### Check if everything works

```bash
# Activate venv first
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux

# Run test script
python test_modules.py full
```

### Expected Output
```
============================================================
Testing Pipeline for: Inception
============================================================

[Step 1] Fetching Reviews...
✓ Fetched 8 reviews

[Step 2] Saving Raw Reviews...
✓ Reviews saved to data/Inception_reviews_raw.csv

[Step 3] Preprocessing Reviews...
✓ Cleaned reviews saved to data/Inception_reviews_clean.csv
✓ Final count: 8 reviews after cleaning

[Step 4] Performing Sentiment Analysis...
✓ Sentiment analysis complete

[Step 5] Calculating Statistics...
✓ Sentiment Statistics:
   total_reviews: 8
   average_sentiment: 0.674
   ...

[Step 6] Getting Sentiment Distribution...
✓ Distribution: {'positive': 6, 'neutral': 1, 'negative': 1}

[Step 7] Creating Visualization...
✓ Sentiment chart saved to plots/Inception_sentiment.png

============================================================
Analysis Complete!
============================================================
```

---

## Troubleshooting Installation

### "Python is not recognized"

**Solution:** Python is not in PATH

**Windows:**
1. Go to Settings → Advanced System Settings
2. Click "Environment Variables"
3. Add Python installation folder to PATH
4. Restart Command Prompt

**Mac/Linux:**
```bash
which python3
# Should show: /usr/bin/python3 or similar
```

### "No module named 'flask'"

**Solution:** Dependencies not installed

```bash
# Make sure venv is activated (see prompt for .venv)
pip install -r requirements.txt
```

### "Port 5000 already in use"

**Solution 1:** Change port in app.py
```python
app.run(port=5001)
```

**Solution 2:** Kill process using the port

**Windows:**
```powershell
Get-Process -Id (Get-NetTCPConnection -LocalPort 5000).OwningProcess | Stop-Process
```

**Mac/Linux:**
```bash
lsof -ti :5000 | xargs kill -9
```

### "venv Scripts not found"

**Solution:** Recreate virtual environment

```bash
# Remove old venv
rm -r .venv  # Mac/Linux
rmdir /s .venv  # Windows

# Create new venv
python -m venv .venv

# Activate and reinstall
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux

pip install -r requirements.txt
```

### "ModuleNotFoundError: No module named 'nltk'"

**Solution:** Reinstall dependencies

```bash
pip install --upgrade nltk
python -c "import nltk; nltk.download('vader_lexicon')"
```

---

## Project Structure

```
letterboxd-review-analyser/
│
├── 📄 Python Files (Backend)
│   ├── app.py                 # Flask application
│   ├── scraper.py            # Web scraping
│   ├── preprocessor.py       # Data cleaning
│   ├── analyzer.py           # Sentiment analysis
│   ├── visualizer.py         # Chart generation
│   ├── config.py             # Configuration
│   ├── test_modules.py       # Testing script
│   │
│   ├── 📁 templates/         # HTML files
│   │   ├── index.html        # Home page
│   │   └── results.html      # Results page
│   │
│   ├── 📁 static/            # Frontend assets
│   │   ├── style.css         # Stylesheet
│   │   ├── script.js         # Home page JS
│   │   └── results.js        # Results page JS
│   │
│   ├── 📁 data/              # Generated data files
│   │   ├── reviews_raw.csv
│   │   ├── reviews_clean.csv
│   │   └── reviews_analyzed.csv
│   │
│   ├── 📁 plots/             # Generated charts
│   │   └── sentiment.png
│   │
│   ├── 📋 Documentation
│   │   ├── README.md         # Project overview
│   │   ├── GUIDE.md          # Detailed guide
│   │   └── requirements.txt  # Dependencies
│   │
│   └── 🔧 Setup Scripts
│       ├── setup.bat         # Windows setup
│       └── setup.sh          # Mac/Linux setup
```

---

## File Descriptions

### Python Backend Files

| File | Purpose |
|------|---------|
| `app.py` | Main Flask application with routes |
| `scraper.py` | Letterboxd web scraping |
| `preprocessor.py` | Text cleaning and preparation |
| `analyzer.py` | NLTK VADER sentiment analysis |
| `visualizer.py` | Matplotlib chart generation |
| `config.py` | Configuration settings |
| `test_modules.py` | Testing and demonstration script |

### Frontend Files

| File | Purpose |
|------|---------|
| `templates/index.html` | Home page with search form |
| `templates/results.html` | Results display page |
| `static/style.css` | Styling (2000+ lines) |
| `static/script.js` | Home page interactivity |
| `static/results.js` | Results page interactivity |

### Configuration Files

| File | Purpose |
|------|---------|
| `requirements.txt` | Production dependencies |
| `requirements-dev.txt` | Development dependencies |
| `config.py` | App configuration |

---

## First Time Usage

### Your First Analysis

1. **Open the app** at http://localhost:5000
2. **Enter a movie name**, e.g., "Inception"
3. **Click "Analyze Reviews"**
4. **Wait for processing** (15-30 seconds)
5. **View results** with sentiment analysis and chart

### What Gets Created

After analysis, check these files:

**Windows:**
```
e:\letterboxd-review-analyser\data\
  - reviews_raw.csv (original data)
  - reviews_clean.csv (cleaned data)
  - reviews_analyzed.csv (with sentiment)

e:\letterboxd-review-analyser\plots\
  - Inception_sentiment.png (chart)
```

**Mac/Linux:**
```
~/letterboxd-review-analyser/data/
  - reviews_raw.csv
  - reviews_clean.csv
  - reviews_analyzed.csv

~/letterboxd-review-analyser/plots/
  - Inception_sentiment.png
```

---

## Development Setup

### Install Development Tools

```bash
pip install -r requirements-dev.txt
```

This adds:
- pytest (testing framework)
- black (code formatter)
- flake8 (linter)
- pylint (code analyzer)

### Format Code

```bash
black *.py  # Formats all Python files
```

### Check Code Quality

```bash
flake8 *.py          # Check for issues
pylint app.py        # Detailed analysis
```

### Run Tests

```bash
pytest test_modules.py -v
```

---

## Deployment Options

### Local Only (Current)
- Accessible at: http://localhost:5000
- Only on your machine

### Local Network
- Modify `app.py`:
```python
app.run(host='0.0.0.0', port=5000)
```
- Access from other machines: http://<your-ip>:5000

### Cloud Deployment

**Heroku (Free):**
```bash
heroku login
heroku create your-app-name
git push heroku main
```

**PythonAnywhere:**
1. Sign up at pythonanywhere.com
2. Upload files
3. Configure WSGI
4. Enable web app

**AWS/Azure:**
- Docker container
- EC2/App Service
- See deployment documentation

---

## Updating Dependencies

```bash
# Check for updates
pip list --outdated

# Update specific package
pip install --upgrade flask

# Update all packages
pip install --upgrade -r requirements.txt
```

---

## Deactivating Virtual Environment

When done working:

```bash
deactivate
```

Your prompt will return to normal (no .venv prefix).

---

## Performance Optimization

### For Faster Processing

1. **Reduce reviews limit**:
   - In `app.py` change `max_reviews=50` to `max_reviews=25`

2. **Disable chart generation**:
   - In `config.py` set `SAVE_CHARTS = False`

3. **Use sample data**:
   - In `config.py` set `USE_SAMPLE_DATA = True`

### For Better Results

1. **Increase reviews limit**:
   - In `app.py` change `max_reviews=50` to `max_reviews=200`

2. **Improve sentiment accuracy**:
   - Use more advanced NLP models (requires additional libraries)

---

## Backup & Restore

### Backup Project

```bash
# Create backup
tar -czf letterboxd-backup.tar.gz letterboxd-review-analyser/

# Or on Windows, use 7-Zip or built-in compression
```

### Clean Generated Files

```bash
# Clear data
rm data/*.csv

# Clear plots
rm plots/*.png

# Keep code, dependencies remain
```

---

## Getting Help

### Resources

- **Python Docs**: https://docs.python.org/3/
- **Flask Documentation**: https://flask.palletsprojects.com/
- **NLTK Guide**: https://www.nltk.org/
- **pandas Tutorials**: https://pandas.pydata.org/docs/

### Common Questions

**Q: Can I run multiple analyses?**
A: Yes! Each analysis overwrites previous data. To save multiple, rename the CSV files.

**Q: How do I add more features?**
A: See GUIDE.md for customization tips.

**Q: Can I use this on production?**
A: Not yet - needs database, authentication, error handling. Great learning project!

**Q: How accurate is the sentiment?**
A: VADER is ~80-85% accurate for reviews. Use with caution for critical decisions.

---

## Next Steps

1. ✅ Complete installation
2. 📖 Read README.md for overview
3. 🎬 Analyze your first movie
4. 📚 Read GUIDE.md for deep dive
5. 🔧 Explore and customize the code
6. 🚀 Deploy or enhance the app

---

## Success Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] NLTK data downloaded
- [ ] App runs without errors
- [ ] Home page loads in browser
- [ ] Test analysis completes successfully
- [ ] Results display correctly
- [ ] Chart is generated

**Once all checked, you're ready to go! 🎉**

---

**Happy analyzing! 🍿📊**
