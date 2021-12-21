"""
Transform data to have more information regarding the news
"""

import argparse
import logging
import pandas as pd

from news_scraping.transform.utils import read_news_from_directory
from news_scraping.transform.cleaning import get_host, sanity_check, hash_uid
from news_scraping.transform.enrichment import tokenize_column
from news_scraping.output import save_data_to_pickle

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def run(input_path: str) -> None:
    """Perform Data wrangling and enrichment"""
    news_df: pd.DataFrame = read_news_from_directory(input_path, suffix='.csv')
    # Data wrangling
    news_df['host'] = get_host(url_col=news_df['url'])
    news_df['uid'] = hash_uid(column=news_df['url'])
    news_df = sanity_check(news_df, subset=['title'])
    news_df['n_tokens_title'] = tokenize_column(news_df, column_name='title')
    news_df['n_tokens_body'] = tokenize_column(news_df, column_name='body')
    save_data_to_pickle(news_df, input_path)


if __name__ == '__main__':
    # load the configuration file
    args_parser = argparse.ArgumentParser()
    # if no input path provided it will take the path from config
    args_parser.add_argument('--inputs', help='Path to input folder', required=False)
    args = args_parser.parse_args()
    input_f: str = args.inputs
    logger.info(f'Reading inputs from: {input_f}')
    run(input_f)
