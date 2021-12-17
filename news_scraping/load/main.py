"""
Transform data to have more information regarding the news
"""

import argparse
import logging
import pandas as pd

from news_scraping.transforn.utils import read_news_from_directory
from news_scraping.transforn.cleaning import get_host, sanity_check, hash_uid
from news_scraping.transforn.enrichment import tokenize_column
from news_scraping.io import save_data_to_pickle

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

# Data enrichment
#   use nlt to analyze natural language


def run(input_path: str) -> None:
    """Perform Data wrangling and enrichment"""
    pass


if __name__ == '__main__':
    # load the configuration file
    args_parser = argparse.ArgumentParser()
    # if no input path provided it will take the path from config
    args_parser.add_argument('--inputs', help='Path to input folder', required=False)
    args = args_parser.parse_args()
    input_f: str = args.inputs
    logger.info(f'Reading inputs from: {input_f}')
    run(input_f)
