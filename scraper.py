"""
Get the news for today from 'la republica' and save them into [today] folder as different txt files
"""

from typing import List

from parser import XPathParser, NewsParser
from store import create_output_folder, save_news_to_folder
from news import News


def run():
    """Get the news for today and save them into [today] folder as different txt files"""
    news_parser: NewsParser = XPathParser()
    # get news links
    news_parser.parse_home()
    # get news information
    news: List[News] = news_parser.parse_news()
    # save news
    output_folder: str = create_output_folder()
    save_news_to_folder(news, output_folder)


if __name__ == '__main__':
    run()
