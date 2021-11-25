"""
Get the news for today from 'la republica' and save them into [today] folder as different txt files
"""
import argparse

from typing import List

from parser import XPathParser, NewsParser
from store import create_output_folder, save_news_to_folder
from news import News
from common import Config


def run():
    """Get the news for today and save them into [today] folder as different txt files"""
    # get arguments from yaml
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('--config_file', help='path to yaml config', default='config.yaml')
    args = args_parser.parse_args()

    # get the configuration from file
    config = Config(args.config_file)
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
