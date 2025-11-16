📊 Twitter/X Stock Market Hashtag Scraper

A complete guide to scraping 2000+ tweets from Twitter/X related to the Indian stock market using Selenium (no API required).

This project automatically extracts tweets for popular trading hashtags such as:

#nifty50

#sensex

#banknifty

#intraday

It scrolls through Twitter/X using browser automation and collects structured tweet data including username, timestamp, content, hashtags, mentions, and engagement metrics.

⭐ Features

🚀 Scrapes 2000+ tweets per hashtag

📌 Works without Twitter/X API

🤖 Uses Selenium to simulate human-like scrolling

📄 Outputs clean structured CSV

🧩 Extracts:

Username

Timestamp

Content

Likes / Replies / Retweets

Hashtags

Mentions

🔍 Supports multiple hashtags in a single run

📚 Table of Contents

Project Overview

How It Works

Installation

Configuration

Running the Scraper

Output Format

Troubleshooting

Disclaimer

📘 Project Overview

This scraper helps analysts, traders, researchers, and developers collect real-time stock market sentiment from Twitter/X.

The tool automates:

Logging into Twitter/X

Searching for stock-related hashtags

Infinite scrolling until enough tweets load

Parsing visible tweets

Exporting to CSV

🛠 How It Works

Selenium WebDriver opens Twitter/X in Chrome

User logs in once (manually)

Script navigates to a hashtag search page

Auto-scrolls and loads new tweets continuously

Parses tweet blocks using BeautifulSoup

Stops when 2000+ tweets are collected

Saves data into a CSV file

This method avoids API restrictions and works reliably at scale.

⚙ Installation
1. Clone the Repository
git clone https://github.com/guptaomkar/x.com-scrapper.git
cd x.com-scrapper

2. Install Required Python Packages
pip install -r requirements.txt

3. Install ChromeDriver

Download a version matching your Chrome browser:

👉 https://chromedriver.chromium.org/downloads

Place it in your project folder or add to PATH.

📝 Configuration
Edit the hashtags you want to scrape:
HASHTAGS = ["#nifty50", "#sensex", "#banknifty", "#intraday"]

Set how many tweets you want:
TWEET_LIMIT = 2000

▶ Running the Scraper

Start the script:

python X_scrapper_hashtags.py

First Run

Chrome will open

Login manually (Twitter requires verification)

The scraper will continue automatically

You do not need to log in again if cookies persist.

📁 Output Format

Your output CSV looks like this:

username	timestamp	content	replies	retweets	likes	mentions	hashtags

Example:

stockguru, 2025-02-12 09:22:14,
"Nifty looks bullish today",
14, 20, 120,
["@nseindia"],
["#nifty50"]


Output file is saved at:

data/stock_tweets.csv

🧪 Troubleshooting
❗ Login page stuck

Clear cookies or login manually on twitter.com before running the script.

❗ Scrolling stops early

Increase waiting time in scroll function:

time.sleep(2.5)

❗ Script not capturing tweets

Ensure UI selectors match the latest Twitter layout.

⚠ Disclaimer

This project is for educational and research purposes only.
Scraping Twitter/X may violate their Terms of Service.
Use responsibly and avoid excessive scraping activity.
