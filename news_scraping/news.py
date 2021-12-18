"""Simple notice object"""

from dataclasses import dataclass, field
from typing import Dict, List, Union
import pandas as pd


@dataclass
class News:
    """Simple structure to store news from a site"""
    title: str
    summary: str
    body: str
    url: str
    date: str = field(default_factory=str)
    site: str = field(default_factory=str)
    host: str = field(default_factory=str)
    uid: str = field(default_factory=str)
    n_tokens_title: int = field(default_factory=int)
    n_tokens_body: int = field(default_factory=int)


class NewsList:
    """Provide methods to interact with News"""
    def __init__(self):
        self._news: List[News] = list()

    def get_news(self) -> List[News]:
        """Get news articles"""
        return self._news

    def append(self, article: News) -> None:
        """Add a new article to news"""
        self._news.append(article)

    def read_from_df(self, df: pd.DataFrame) -> None:
        """Read news from pandas dataframe"""
        for _, row in df.iterrows():
            attrs: Dict[str, str] = {attr: row[attr] for attr in News.__annotations__}
            self.append(News(**attrs))
