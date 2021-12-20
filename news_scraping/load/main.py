"""
Load data into a database
"""

import argparse
import logging
import pandas as pd
import dataclasses
from sqlalchemy.exc import IntegrityError

from news_scraping.load.utils import read_news_from_pickles
from news_scraping.news import NewsList
from news_scraping.load.db.article import DataBaseConnection, Article

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def run(input_path: str) -> None:
    """Save data into a database"""
    # configure database
    conn = DataBaseConnection(input_path)
    conn.Base.metadata.create_all(conn.engine)
    # Read data
    news: pd.DataFrame = read_news_from_pickles(input_path)
    news_list = NewsList()
    news_list.read_from_df(news)
    # save data to database
    with conn.Session.begin() as session:
        for art in news_list.get_news():
            logger.info(f'Loading article uid {art.uid} into DB')
            article = Article(**dataclasses.asdict(art))
            try:
                session.add(article)
            except IntegrityError as e:
                logger.error(f'Error: {e}')


if __name__ == '__main__':
    # load the configuration file
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('--inputs', help='Path to input folder', required=True)
    args = args_parser.parse_args()
    input_f: str = args.inputs
    logger.info(f'Reading inputs from: {input_f}')
    run(input_f)
