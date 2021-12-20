"""Run all the steps with a single file"""

import argparse
import logging
from typing import Dict
import news_scraping.extract.main as extract
import news_scraping.transform.main as transform
import news_scraping.load.main as load

from news_scraping.common import Config, Site

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run(config: Config):
    """Run all the steps"""
    sites: Dict[str, Site] = config.sites
    o_folder: str = config.output_folder

    # Run all the steps
    extract.run(sites, output_folder=o_folder)
    transform.run(o_folder)
    load.run(o_folder)
    logger.info('Finished with processing')


if __name__ == '__main__':
    # load the configuration file
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('--config_file', help='path to yaml config', default='config.yaml')
    args = args_parser.parse_args()

    # get the configuration from file
    cfg = Config(args.config_file)
    run(cfg)
