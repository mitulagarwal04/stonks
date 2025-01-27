# /src/scraper/moneycontrol_scraper.py
import requests
from bs4 import BeautifulSoup
import os
import pandas as pd 
from pathlib import Path


def scrape_moneycontrol():
    url = 
    response = 
    soup = 

    articles = []
    for item in soup.select("")
    headline = 
    timestamp = 
    link = 
    articles.append({
        "headlines":headline,
        "timestamp":timestamp,
        "url":link,
        "source":'moneycontrol'
    })

    raw_path = Path("data/raw/new/moneycontrol.csv")
    # pd.DataFrame(articles).to_csv(raw_path, mode='a', header='not')  check this one what it is
    print(f"Scraped {len(articles)} articles from MoneyControl ..... ")

if __name__=="__main__":
    scrape_moneycontrol()