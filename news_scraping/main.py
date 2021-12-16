"""
Get the news for today from 'la republica' and save them into [today] folder as different txt files
"""
import argparse
import logging

from typing import List

from news_scraping.store import create_output_folder, save_news_to_txt, save_news_to_csv
from news_scraping.news import News
from news_scraping.common import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run(config: Config):
    """Get the news for today and save them into [today] folder as different txt files"""
    # n_parser: NewsParser = XPathParser()
    # get news for all the different folders
    for site_name, site in config.sites.items():
        logger.info(f'--- Parsing data from {site_name} ---')
        site.parser(config)     # type: ignore
        site_news: List[News] = site.parser.parse_news()
        # save news
        output_folder: str = create_output_folder(site_name)
        logger.info(f'Saving results to: {output_folder}')

        save_news_to_txt(site_news, output_folder)
        save_news_to_csv(site_news, output_folder)


if __name__ == '__main__':
    # get arguments from yaml
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('--config_file', help='path to yaml config', default='config.yaml')
    args = args_parser.parse_args()

    # get the configuration from file
    cfg = Config(args.config_file)
    logger.info(f'Beginning scraper for {cfg.sites}')
    run(cfg)
