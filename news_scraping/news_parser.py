"""Contains different parsers like beautiful soup and xpath"""

# TODO: separate page parser into two different parsers: one for home an the other for news
import requests
import bs4
import logging

import lxml.html as html

from abc import ABC, abstractmethod
from typing import List, Set

from news_scraping.news import News
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

    def get_news_details(self, news_page: bs4.BeautifulSoup) -> News:
        """Get the details from news page and return a News object"""
        title = self._get_news_title(news_page)
        summary = self._get_news_summary(news_page)
        body = self._get_news_body(news_page)
        return News(title, summary, body)

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
        self._config: common.Config
        self._site: common.Site
        self._news_home: List[str]

    def __call__(self, config: common.Config):
        """Parse data. This is done to have __init__ without arguments"""
        self._config = config
        self._site = self._config.sites['eluniversal']
        self._news_home = self.parse_home()

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
        news_details: List[News] = list()
        for i, news_url in enumerate(self._news_home):
            logger.info(f'({i + 1} / {len(self._news_home)}) - Parsing data from: {news_url} ...')
            response_news: requests.Response = requests.get(news_url)
            if not response_news.status_code == 200:
                logger.warning(f'--- Failed to parse!')
                continue
            news_page = bs4.BeautifulSoup(response_news.text, 'html.parser')
            news_details.append(self.get_news_details(news_page))
            logger.info(f'--- SUCCESS!')

        return news_details


class ElPaisParser(NewsParser):
    @property
    def site(self) -> common.Site:
        pass

    def parse_home(self) -> List[str]:
        pass

    def parse_news(self) -> List[News]:
        pass


class XPathParser(NewsParser):
    @property
    def site(self) -> common.Site:
        pass

    HOME_URL = 'https://www.larepublica.co/'

    XPATH_LINK_TO_ARTICLE = '//text-fill/a[@class="economiaSect" or @class="empresasSect" or @class="ocioSect" ' \
                            'or @class="globoeconomiaSect" or @class="analistas-opinionSect"]/@href'
    XPATH_TITTLE = '//div[@class="mb-auto"]/text-fill/span/text()'
    XPATH_SUMMARY = '//div[@class="lead"]/p/text()'
    XPATH_BODY = '//div[@class="html-content"]/p[not(@class)]/text()'

    def __init__(self):
        """Setup variables"""
        self.parsed_home: html.HtmlElement
        self.linked_news: List[str]
        self.news: List[News]

    def parse_home(self) -> List[str]:
        """Get list of news"""
        response_home: requests.Response = requests.get(self.HOME_URL)
        if response_home.status_code == 200:
            home: str = response_home.content.decode('utf-8')
            self.parsed_home = html.fromstring(home)
            self.linked_news = self.parsed_home.xpath(self.XPATH_LINK_TO_ARTICLE)
            return self.linked_news
        else:
            raise ValueError(f"Response from {self.HOME_URL}: {response_home}")

    def parse_title(self, parsed_news: html.HtmlElement) -> str:
        """parse title for news"""
        title: str = parsed_news.xpath(self.XPATH_TITTLE)[0]
        return title.replace('\"', '')

    def parse_summary(self, parsed_news: html.HtmlElement) -> str:
        """parse summary from news"""
        return str(parsed_news.xpath(self.XPATH_SUMMARY)[0])

    def parse_body(self, parsed_news: html.HtmlElement) -> str:
        """parse body from news"""
        return ' '.join(parsed_news.xpath(self.XPATH_BODY))

    def parse_news(self) -> List[News]:
        """Get notices from links and return a list of notices"""
        for news_link in self.linked_news:
            try:
                response: requests.Response = requests.get(news_link)
                if response.status_code == 200:
                    notice: str = response.content.decode('utf-8')
                    parsed: html.HtmlElement = html.fromstring(notice)

                    try:
                        title: str = self.parse_title(parsed)
                        summary: str = self.parse_summary(parsed)
                        body: str = self.parse_body(parsed)
                        self.news.append(News(title, summary, body))
                    except IndexError:
                        print(f'No news from: {news_link}')
                        continue
            except ValueError as ve:
                print(ve)
        return self.news
