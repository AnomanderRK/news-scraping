"""
Load data into a database
"""

import argparse
import logging
import pandas as pd
import dataclasses

from news_scraping.load.utils import read_news_from_pickles
from news_scraping.news import NewsList
from news_scraping.load.db.article import Base, engine, Session, Article

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def run(input_path: str) -> None:
    """Save data into a database"""
    # configure database
    Base.metadata.create_all(engine)
    # Read data
    news: pd.DataFrame = read_news_from_pickles(input_path)
    news_list = NewsList()
    news_list.read_from_df(news)
    # save data to database
    with Session() as session:
        with session.begin():
            for art in news_list.get_news():
                logger.info(f'Loading article uid {art.uid} into DB')
                article = Article(**dataclasses.asdict(art))
                try:
                    session.add(article)
                except Exception as e:
                    logger.error(f'Error: {e}')
                    logger.error(f'Article: {art}')


if __name__ == '__main__':
    # load the configuration file
    args_parser = argparse.ArgumentParser()
    # if no input path provided it will take the path from config
    args_parser.add_argument('--inputs', help='Path to input folder', required=False)
    args = args_parser.parse_args()
    input_f: str = args.inputs
    logger.info(f'Reading inputs from: {input_f}')
    run(input_f)
