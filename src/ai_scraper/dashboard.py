import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql://scraper:secret@localhost:5432/scraped_data")

st.title("AI Scraping Agent Monitor")
st.write("### Real-time Stats")

df = pd.read_sql("SELECT domain, COUNT(*) as count FROM articles GROUP BY domain", engine)
st.bar_chart(df.set_index("domain"))

st.write("### Recent Scraped Data")
domain = st.selectbox("Choose Domain", df.domain.tolist())
data = pd.read_sql(f"SELECT title, url FROM articles WHERE domain = '{domain}' LIMIT 20", engine)
st.dataframe(data)