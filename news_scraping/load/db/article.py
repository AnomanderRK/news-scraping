"""Handle database connections and interactions"""
import os

from sqlalchemy import Column, String, Integer, DateTime

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from news_scraping.output import create_output_folder


class DataBaseConnection:
    """Configure database connection"""
    Base = declarative_base()

    def __init__(self, folder: str, database_name: str = 'newspaper.db'):
        """Create database connection"""
        self.database_path: str = os.path.join(folder, database_name)
        create_output_folder(folder)
        self.engine = create_engine(f'sqlite:///{self.database_path}')
        self.Session = sessionmaker(bind=self.engine)


class Article(DataBaseConnection.Base):     # type: ignore
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
