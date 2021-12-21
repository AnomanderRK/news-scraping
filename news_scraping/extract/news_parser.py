"""Contains different parsers like beautiful soup and xpath"""
from __future__ import annotations      # resolve circular dependency with hints

import requests
import bs4
import logging

import lxml.html as html

from abc import ABC, abstractmethod
from typing import List, Set

from news_scraping.news import News, NewsList
from news_scraping import common

logger = logging.getLogger(__name__)


class NewsParser(ABC):
    @abstractmethod
    def parse_home(self) -> List[str]:
        """Get list of news from home"""

    @abstractmethod
    def parse_news(self) -> List[News]:
        """Get news"""

    @property
    @abstractmethod
    def site(self) -> common.Site:
        """Get the Site object used"""

    @property
    @abstractmethod
    def news(self) -> NewsList:
        """Get the Site object used"""

    def get_news_details(self, news_page: bs4.BeautifulSoup, news_url: str) -> News:
        """Get the details from news page and return a News object"""
        title = self._get_news_title(news_page)
        summary = self._get_news_summary(news_page)
        body = self._get_news_body(news_page)
        return News(title, summary, body, news_url)

    def _get_news_title(self, news_page: bs4.BeautifulSoup) -> str:
        """Get the news title from news page"""
        for result in common.select_query(self.site.queries['news_title'], news_page):
            return str(result.text.strip())
        return 'No title found'

    def _get_news_summary(self, news_page: bs4.BeautifulSoup) -> str:
        """Get the news summary from news page"""
        for result in common.select_query(self.site.queries['news_summary'], news_page):
            return str(result.text.strip())
        return 'No summary found'

    def _get_news_body(self, news_page: bs4.BeautifulSoup) -> str:
        """Get the news body from news page"""
        body_text: List[str] = list()
        for result in common.select_query(self.site.queries['news_body'], news_page):
            body_text.append(result.text.strip())
        return '\n'.join(body_text)


class ElUniversalParser(NewsParser):
    """Read news from el universal news"""
    def __init__(self):
        """get the universal site info initialization"""
        self._site: common.Site
        self._news_home: List[str]
        self._news: NewsList = NewsList()

    def __call__(self, site: common.Site):
        """Parse data. This is done to have __init__ without arguments"""
        self._site = site
        self._news_home = self.parse_home()

    @property
    def news(self) -> NewsList:
        return self._news

    @property
    def site(self) -> common.Site:
        return self._site

    def _get_news_from_home(self, home: bs4.BeautifulSoup) -> List[str]:
        """Get list of news"""
        links_set: Set[str] = set()     # use a set to get unique values
        for link in common.select_query(self._site.homepage_links_query, home):
            if link and link.has_attr('href'):
                links_set.add(link['href'])
        logger.info(f'Found: {len(links_set)} different news')
        return list(links_set)

    def parse_home(self) -> List[str]:
        """Parse news from home"""
        response_home: requests.Response = requests.get(self._site.url)
        if not response_home.status_code == 200:
            logger.warning(f'Could not parse data from {self._site.url}')
            return list([f'Invalid response from {self._site.url}'])
        home = bs4.BeautifulSoup(response_home.text, 'html.parser')
        logger.info(f'Getting news from: {self._site.url}')
        return self._get_news_from_home(home)

    def parse_news(self) -> List[News]:
        """Get news from home return a list of News objects"""
        for i, news_url in enumerate(self._news_home):
            logger.info(f'({i + 1} / {len(self._news_home)}) - Parsing data from: {news_url} ...')
            response_news: requests.Response = requests.get(news_url)
            if not response_news.status_code == 200:
                logger.warning('--- Failed to parse!')
                continue
            news_page = bs4.BeautifulSoup(response_news.text, 'html.parser')
            self._news.append(self.get_news_details(news_page, news_url))
            logger.info('--- SUCCESS!')

        return self._news.get_news()
