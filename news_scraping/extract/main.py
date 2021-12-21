"""
---
Extract data
---

Get the news for today from different news sites and save them into [today] folder as different txt files
"""
import argparse
import logging

from typing import List, Dict

from news_scraping.output import create_output_folder_from_site, save_news_to_csv
from news_scraping.news import News
from news_scraping.common import Config, Site

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run(sites: Dict[str, Site], output_folder: str):
    """Get the news for today and save them into [today] folder as different txt files"""
    # get news for all the different folders
    for site_name, site in sites.items():
        site.parser(site)     # type: ignore
        site_news: List[News] = site.parser.parse_news()
        # save news in specific folder
        output_folder: str = create_output_folder_from_site(output_folder, site_name)
        # save_news_to_txt(site_news, output_folder)
        save_news_to_csv(site_news, output_folder)


if __name__ == '__main__':
    # get arguments from yaml
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('--config_file', help='path to yaml config', default='config.yaml')
    args = args_parser.parse_args()

    # get the configuration from file
    cfg = Config(args.config_file)
    sites_: Dict[str, Site] = cfg.sites
    o_folder: str = cfg.output_folder
    logger.info(f'Beginning scraper for: {sites_}')
    logger.info(f'Output folder: {o_folder}')
    run(sites_, o_folder)
