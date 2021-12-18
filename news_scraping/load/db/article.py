"""Handle database connections and interactions"""

from sqlalchemy import Column, String, Integer, DateTime

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///newspaper.db')
Session = sessionmaker(bind=engine)
Base = declarative_base()


class Article(Base):
    __tablename__ = 'articles'

    uid = Column(String, primary_key=True)
    title = Column(String)
    summary = Column(String)
    body = Column(String)
    url = Column(String)
    date = Column(DateTime)
    site = Column(String)
    host = Column(String)
    n_tokens_title = Column(Integer)
    n_tokens_body = Column(Integer)

    def __init__(self, uid, title: str, summary: str,
                 body: str, url: str, date: str, site: str,
                 host: str, n_tokens_title: int, n_tokens_body: int):
        self.uid = uid
        self.title = title
        self.summary = summary
        self.body = body
        self.url = url
        self.date = date
        self.site = site
        self.host = host
        self.n_tokens_title = n_tokens_title
        self.n_tokens_body = n_tokens_body
