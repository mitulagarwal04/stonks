# src/scraper/newsapi_fetcher.py

import pandas
import os
from dotenv import load_dotenv
from newapi import NewsApiClient

load_dotenv()
newsapi = NewsApiClient(api_key = os.getenv("NEWSAPI_KEY"))

def fetch_newsapi(query = ""):
    articles = newsapi.get_everything(
        q = query,
        language = 'en',
        sort_by = 'publishedAt',
        page_size = 100 
    )['articles']

    df = pd.DataFrame([{
            "headline":a['title'],
            "timestamp":a['publishedAt'],
            "url":a['url'],
            "source":"newsapi"
        } for a in articles ])

    df.to_csv('data/raw/news/newsapi.csv', index=False, mode='a', header=False)
    print(f"fetched {len(articles)} articles from NewsAPI ... ")

if __name__=="__main__":
    fetch_newsapi()

