import time
import pickle
from pathlib import Path
from datetime import datetime, timedelta
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

COOKIE_FILE = "twitter_cookies.pkl"
HASHTAGS = ["nifty50", "sensex", "intraday", "banknifty"]
TARGET_COUNT = 2000

# ----------------- Create Chrome Driver -----------------

def create_driver():
    options = uc.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--start-maximized")
    return uc.Chrome(version_main=140, options=options)

# ----------------- Login & Cookies -----------------

def login_and_save_cookies(driver):
    print("\n🔵 No cookie file found. Opening login page...")
    driver.get("https://twitter.com/login")
    time.sleep(20)  # User logs in manually
    print("🟢 Logged in. Saving cookies...")
    pickle.dump(driver.get_cookies(), open(COOKIE_FILE, "wb"))
    print("✔ Cookies saved.\n")

def load_cookies(driver):
    print("🔵 Loading cookies...")
    driver.get("https://twitter.com")
    cookies = pickle.load(open(COOKIE_FILE, "rb"))
    for cookie in cookies:
        try:
            driver.add_cookie(cookie)
        except:
            pass
    driver.refresh()
    time.sleep(5)
    print("🟢 Session restored.\n")

# ----------------- Extract Tweet Info -----------------

def extract_tweet_data(article):
    try:
        content = article.text
        parts = content.split("\n")

        # Username and handle
        username = parts[0] if parts else ""
        handle = parts[1] if len(parts) > 1 else ""

        # Content text
        body = " | ".join(parts[2:-3]).strip()

        # Engagement numbers (taken from footer)
        footer = parts[-3:]
        replies = footer[0] if len(footer) > 0 else "0"
        retweets = footer[1] if len(footer) > 1 else "0"
        likes = footer[2] if len(footer) > 2 else "0"

        # Hashtags
        hashtags = [w for w in body.split() if w.startswith("#")]

        # Mentions
        mentions = [w for w in body.split() if w.startswith("@")]

        # Timestamp extraction (from `<time>` tag)
        timestamp = ""
        try:
            time_tag = article.find_element(By.TAG_NAME, "time")
            timestamp = time_tag.get_attribute("datetime")
        except:
            pass

        # Convert timestamp to IST
        if timestamp:
            dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            dt_ist = dt + timedelta(hours=5, minutes=30)
            timestamp = dt_ist.strftime("%Y-%m-%d %H:%M:%S")

        return {
            "username": username,
            "handle": handle,
            "timestamp": timestamp,
            "content": body,
            "replies": replies,
            "retweets": retweets,
            "likes": likes,
            "hashtags": ", ".join(hashtags),
            "mentions": ", ".join(mentions),
        }

    except:
        return None

# ----------------- Scrape Hashtags -----------------

def scrape_hashtag(driver, hashtag, target_count):
    print(f"🔍 Scraping #{hashtag} ...")
    url = f"https://twitter.com/search?q=%23{hashtag}&f=live"
    driver.get(url)
    time.sleep(5)

    collected = []
    seen = set()
    last_height = driver.execute_script("return document.body.scrollHeight")
    cutoff_time = datetime.now() - timedelta(hours=24)

    while len(collected) < target_count:
        tweets = driver.find_elements(By.XPATH, "//article")

        for t in tweets:
            data = extract_tweet_data(t)
            if not data:
                continue

            # Avoid duplicates
            key = data["timestamp"] + data["content"]
            if key in seen:
                continue
            seen.add(key)

            # Filter only last 24 hours
            if data["timestamp"]:
                tweet_time = datetime.strptime(data["timestamp"], "%Y-%m-%d %H:%M:%S")
                if tweet_time < cutoff_time:
                    continue

            collected.append(data)
            print(f"👉 Collected: {len(collected)} tweets", end="\r")

            if len(collected) >= target_count:
                break

        # Scroll
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print("\n⚠ No more tweets loading.")
            break
        last_height = new_height

    print(f"\n✅ #{hashtag} → {len(collected)} tweets collected.")
    return collected

# ----------------- Main Program -----------------

driver = create_driver()

if Path(COOKIE_FILE).exists():
    load_cookies(driver)
else:
    login_and_save_cookies(driver)

all_tweets = []

for tag in HASHTAGS:
    tweets = scrape_hashtag(driver, tag, TARGET_COUNT)
    all_tweets.extend(tweets)

driver.quit()

# ----------------- Save Output -----------------

import csv

with open("stock_tweets.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "Username", "Handle", "Timestamp", "Content",
        "Replies", "Retweets", "Likes",
        "Hashtags", "Mentions"
    ])
    for t in all_tweets:
        writer.writerow([
            t["username"], t["handle"], t["timestamp"], t["content"],
            t["replies"], t["retweets"], t["likes"],
            t["hashtags"], t["mentions"]
        ])

print("\n📁 Saved: stock_tweets.csv")
print(f"📊 Total tweets collected: {len(all_tweets)}")
