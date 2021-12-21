"""Functions and helpers for data transformation"""

import pandas as pd
import os

from typing import List, Dict, Callable, Union
from datetime import datetime

from news_scraping.output import read_news_from_txt, read_news_from_csv


def get_date_time_from_string(path: str, pattern='%d-%m-%Y') -> Union[datetime, None]:
    """Get date time from str"""
    for candidate in path.split('\\')[::-1]:
        try:
            date: datetime = datetime.strptime(candidate, pattern)
            return date
        except ValueError:
            # No matching pattern
            pass
    return None


def read_news_from_directory(folder: str, suffix: str = '.csv') -> pd.DataFrame:
    """
    Read news from 'suffix' files in folder and return a dataframe with all the data

    store the directories in folder as new columns in dataframe

    Expecting:
    folder/site_name/date/files
    """
    # map a file type to a function to read data
    suffix_map: Dict[str, Callable[[str], pd.DataFrame]] = {
        '.csv': read_news_from_csv,
        '.txt': read_news_from_txt
    }
    get_news: Callable[[str], pd.DataFrame] = suffix_map[suffix]
    sites: List[str] = [d for d in os.listdir(folder)
                        if os.path.isdir(os.path.join(folder, d))]
    # store all the data in a single dataframe
    news_df = pd.DataFrame()
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(suffix):
                news: pd.DataFrame = get_news(os.path.join(root, file))
                # add directories as column values
                news['date'] = get_date_time_from_string(root)
                news['site'] = [s for s in sites if s in root][0]
                news_df = news_df.append(news)
    return news_df
