"""Functions to clean data from news dataframe"""

import hashlib
import logging
import pandas as pd
from urllib.parse import urlparse
from typing import List, Optional

logger = logging.getLogger(__name__)


def get_host(url_col: pd.Series) -> pd.Series:
    """Get host from url col"""
    logger.info('Getting host name')
    return url_col.apply(lambda url: urlparse(url).netloc)


def sanity_check(news_df: pd.DataFrame, subset: Optional[List[str]] = None) -> pd.DataFrame:
    """Handle missing and duplicated titles on subset if provided"""
    logger.info('Performing sanity check')
    news_df = news_df.drop_duplicates(subset=subset)
    news_df = news_df.dropna(subset=subset)
    return news_df


def hash_uid(column: pd.Series) -> pd.Series:
    """Hash column using hashlib"""
    logger.info('Creating hash uid')
    uid: pd.Series = (column
                      .apply(lambda item: hashlib.md5(bytes(str(item).encode())))
                      .apply(lambda hash_object: hash_object.hexdigest()))
    return uid

