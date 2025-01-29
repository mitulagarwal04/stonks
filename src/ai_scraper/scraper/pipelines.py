from sqlalchemy import create_engine, Column, String, Text, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionsmaker

Base = declarative_base()

class article(Base):
    __tablename__="articles"
    id = Column(String, primary_key=True)
    title = Column(string)
    content = Column(Text)
    domain = Column(String)
    published_date = Column(TIMESTAMP)
    url = Column(String)

class PostgresPipeline:
    def __init__(self):
        self.engine = create_engine("postgresql://scraper:secret@localhost:5432/scraped_data")
        Base.metadata.create_all(self.engine)
        self.Session = sessionsmaker(bind=self.engine)

    def process_item(self, item, spider):
        session = self.Session
        article = Article(
            id = item["url"],
            title = item.get("title"),
            content = item.get("content"),
            domain = item.get("domain"),
            published_date = item.get("published_date"),
            url = item["url"]
        )
    session.merge(article)
    session.commit()
    return item
