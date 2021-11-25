"""Contains different parsers like beautiful soup and xpath"""

# TODO: separate page parser into two different parsers: one for home an the other for news
import requests

import lxml.html as html

from abc import ABC, abstractmethod
from typing import List

from news import News


class NewsParser(ABC):
    @abstractmethod
    def parse_home(self) -> List[str]:
        """Get list of news from home"""

    @abstractmethod
    def parse_news(self) -> List[News]:
        """Get news"""


class ElUniversalParser(NewsParser):
    """Read news from el universal news"""
    def __init__(self):
        pass

    def parse_home(self) -> List[str]:
        ...

    def parse_news(self) -> List[News]:
        ...


class XPathParser(NewsParser):
    HOME_URL = 'https://www.larepublica.co/'

    XPATH_LINK_TO_ARTICLE = '//text-fill/a[@class="economiaSect" or @class="empresasSect" or @class="ocioSect" ' \
                            'or @class="globoeconomiaSect" or @class="analistas-opinionSect"]/@href'
    XPATH_TITTLE = '//div[@class="mb-auto"]/text-fill/span/text()'
    XPATH_SUMMARY = '//div[@class="lead"]/p/text()'
    XPATH_BODY = '//div[@class="html-content"]/p[not(@class)]/text()'

    def __init__(self):
        """Setup variables"""
        self.parsed_home = None
        self.linked_news = None
        self.news: List[News] = list()

    def parse_home(self) -> List[str]:
        """Get list of news"""
        response_home: requests.Response = requests.get(self.HOME_URL)
        if response_home.status_code == 200:
            home: str = response_home.content.decode('utf-8')
            self.parsed_home: html.HtmlElement = html.fromstring(home)
            self.linked_news: List[str] = self.parsed_home.xpath(self.XPATH_LINK_TO_ARTICLE)
            return self.linked_news
        else:
            raise ValueError(f"Response from {self.HOME_URL}: {response_home}")

    def parse_title(self, parsed_news: html.HtmlElement) -> str:
        """parse title for news"""
        title: str = parsed_news.xpath(self.XPATH_TITTLE)[0]
        return title.replace('\"', '')

    def parse_summary(self, parsed_news: html.HtmlElement) -> str:
        """parse summary from news"""
        return parsed_news.xpath(self.XPATH_SUMMARY)[0]

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
