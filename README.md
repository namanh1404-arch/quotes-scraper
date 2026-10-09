# Quotes Scraper

A simple web scraper that extracts quotes from quotes.toscrape.com.

## Features
- Scrapes all 10 pages of quotes
- Saves data to CSV with proper encoding
- Handles connection errors gracefully

## Tech Stack
- Python
- requests
- BeautifulSoup4

## How to Run
1. Clone this repo
2. Create virtual environment: `python -m venv .venv`
3. Activate: `source .venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run: `python scraper.py`

## Output
A `quotes.csv` file with columns: STT, Author, Quote.

## What I Learned
- Basic HTTP requests with `requests`
- HTML parsing with BeautifulSoup
- CSV file handling
- Error handling and logging
