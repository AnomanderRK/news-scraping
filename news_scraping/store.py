"""methods to save results"""

import os
import datetime
import logging
import pandas as pd
from pathvalidate import sanitize_filepath

from typing import List, Union, Dict
from news_scraping.news import News

logger = logging.getLogger(__name__)


def create_output_folder(site: str) -> str:
    """Create output folder for site, if it does not exists and return it"""
    today: str = datetime.date.today().strftime('%d-%m-%Y')
    o_folder: str = os.path.join(os.getcwd(), today, site)
    if not os.path.isdir(o_folder):
        os.makedirs(o_folder)
    return o_folder


def format_output_name(output_folder: str, title: str, identifier: Union[int, str] = '', name_max_len: int = 50) -> str:
    """format output name in he following way: output_folder/tile/identifier"""
    title = title.strip().replace(' ', '_').replace("'", '"').replace("/", '')
    clean_title = sanitize_filepath(title, max_len=name_max_len)
    output_file = os.path.join(output_folder, f'{identifier}_{clean_title}')
    return output_file


def save_news_to_txt(news: List[News], output_folder: str):
    """Save results into output folder"""
    for i, new in enumerate(news):
        output_file_name: str = format_output_name(output_folder, new.title, i)
        with open(f'{output_file_name}.txt', 'w', encoding='utf-8') as f:
            # write the news
            f.write(new.title)
            f.write('\n\n')
            f.write('\n\n')
            f.write(f'{new.summary}')
            f.write('\n\n')
            f.write(f'{new.body}')
            f.write('\n\n')

    logger.info('Saving results finished!')


def save_news_to_csv(news: List[News], output_folder: str, file_name: str = '_consolidated_news.csv') -> None:
    """Save results to one, unique, csv file_name.csv"""
    output_file_name: str = format_output_name(output_folder=output_folder, title=file_name)
    # Create a column per attribute (not special)
    cols: List[str] = [attr for attr in News.__annotations__]
    data_dict: Dict[str, List[str]] = {col: [] for col in cols}
    for n in news:
        for col in cols:
            data_dict[col].append(getattr(n, col))
    data_df = pd.DataFrame(data_dict)
    data_df.to_csv(output_file_name, index=False)
