import pandas as pd
import os

import logging

logger = logging.getLogger(__name__)


def read_news_from_pickles(folder: str, suffix: str = '.pkl') -> pd.DataFrame:
    """
    Read news from 'suffix' files in folder and return a dataframe with all the data
    """
    # store all the data in a single dataframe
    news_df = pd.DataFrame()
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(suffix):
                f: str = os.path.join(root, file)
                logger.info(f'Reading data from: {f}')
                news: pd.DataFrame = pd.read_pickle(f)
                news_df = news_df.append(news)
    return news_df
