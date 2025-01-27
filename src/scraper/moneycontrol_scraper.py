# /src/scraper/moneycontrol_scraper.py
#
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import sqlalchemy as db
from tenacity import retry, stop_after_attempt, wait_exponential
from fake_useragent import UserAgent
import time
import logging

# Configure logging
logging.basicConfig(filename='scraper.log', level=logging.INFO)

# SQL Setup (SQLite Example)
engine = db.create_engine('sqlite:///news.db')
metadata = db.MetaData()
news_table = db.Table(
    'news', metadata,
    db.Column('id', db.Integer, primary_key=True),
    db.Column('headline', db.Text),
    db.Column('news', db.Text),
    db.Column('timestamp', db.DateTime),
    db.Column('url', db.String(255)),
    db.Column('category', db.String(50))
)
metadata.create_all(engine)

# Proxy Setup (Free proxies with fallback)
def get_proxy():
    try:
        response = requests.get("https://free-proxy-list.net/")
        soup = BeautifulSoup(response.text, 'html.parser')
        proxies = [f"{row.td.text}:{row.td.find_next_sibling().text}" 
                   for row in soup.select('tbody tr')[:10]]
        return {'http': f'http://{proxies[0]}', 'https': f'http://{proxies[0]}'}
    except:
        return None

# User Agent Rotation
ua = UserAgent()

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1))
def fetch_url(url):
    headers = {'User-Agent': ua.random}
    proxy = get_proxy()
    try:
        response = requests.get(url, headers=headers, proxies=proxy, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed {url}: {e}")
        raise

def get_categories(base_url):
    html = fetch_url(base_url)
    soup = BeautifulSoup(html, 'html.parser')
    nav = soup.find('nav', {'class': 'clearfix'})  # Update selector based on actual structure
    categories = [urljoin(base_url, a['href']) for a in nav.find_all('a')]
    return list(set(categories))  # Deduplicate

def scrape_articles(category_url):
    page_num = 1
    while True:
        page_url = f"{category_url.rstrip('/')}/page-{page_num}/"
        html = fetch_url(page_url)
        soup = BeautifulSoup(html, 'html.parser')
        
        # Stop if no articles
        articles = soup.find_all('li', {'class': 'clearfix'})  # Update selector
        if not articles:
            break
        
        for article in articles:
            link = article.find('a', href=True)
            if link:
                yield urljoin(category_url, link['href'])
        
        page_num += 1

def parse_article(article_url, category):
    html = fetch_url(article_url)
    soup = BeautifulSoup(html, 'html.parser')
    
    # Critical: Update these selectors after inspecting the page
    headline = soup.find('h1', {'class': 'artTitle'}).text.strip()
    timestamp = soup.find('div', {'class': 'article_schedule'}).text.strip()
    body = ' '.join([p.text for p in soup.find('div', {'class': 'content_wrapper'}).find_all('p')])
    
    return {
        'headline': headline,
        'news': body,
        'timestamp': timestamp,  # Convert to datetime later
        'url': article_url,
        'category': category
    }

# HTML Structure Monitor
def structure_check(html):
    soup = BeautifulSoup(html, 'html.parser')
    critical_selectors = ['h1.artTitle', 'div.article_schedule', 'div.content_wrapper']
    for selector in critical_selectors:
        if not soup.select_one(selector):
            raise ValueError(f"Selector {selector} not found! HTML may have changed.")

# Main Script
def main():
    base_url = "https://www.moneycontrol.com/news/"
    categories = get_categories(base_url)
    
    for category_url in categories:
        category_name = category_url.split('/')[-2]
        try:
            for article_url in scrape_articles(category_url):
                try:
                    article_data = parse_article(article_url, category_name)
                    
                    # Save to JSON (split by category/date)
                    with open(f"{category_name}_{time.strftime('%Y-%m')}.json", 'a') as f:
                        f.write(json.dumps(article_data) + '\n')
                    
                    # Save to SQL
                    with engine.connect() as conn:
                        conn.execute(news_table.insert().values(**article_data))
                    
                    # Add minimal delay (0.5s)
                    time.sleep(0.5)
                
                except Exception as e:
                    logging.error(f"Article {article_url} failed: {e}")
                    continue
        except Exception as e:
            logging.error(f"Category {category_url} failed: {e}")
            continue

if __name__ == "__main__":
    main()