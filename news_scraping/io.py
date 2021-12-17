"""methods to save results"""

import os
import datetime
import logging
import pandas as pd
from pathvalidate import sanitize_filepath

from typing import List, Union, Dict
from news_scraping.extract.news import News

logger = logging.getLogger(__name__)


def create_output_folder(output_folder: str) -> str:
    """Create output folder if not available and return it"""
    if not os.path.isdir(output_folder):
        os.makedirs(output_folder)
    return output_folder


def create_output_folder_from_site(output_path: str, site: str) -> str:
    """Create output folder for site, if it does not exists, and return it"""
    today: str = datetime.date.today().strftime('%d-%m-%Y')
    o_folder: str = os.path.join(output_path, site, today)
    return create_output_folder(o_folder)


def format_output_name(output_folder: str, title: str, identifier: Union[int, str] = '', name_max_len: int = 50) -> str:
    """format output name in he following way: output_folder/tile/identifier"""
    title = title.strip().replace(' ', '_').replace("'", '"').replace("/", '')
    clean_title = sanitize_filepath(title, max_len=name_max_len)
    output_file = os.path.join(output_folder, f'{identifier}_{clean_title}')
    return output_file


def save_news_to_txt(news: List[News], output_folder: str):
    """Save results into output folder"""
    logger.info(f'Saving individual results to: {output_folder}')
    # one row per attribute
    attrs: List[str] = [attr for attr in News.__annotations__]
    for i, new in enumerate(news):
        output_file_name: str = format_output_name(output_folder, new.title, i)
        with open(f'{output_file_name}.txt', 'w', encoding='utf-8') as f:
            for attr in attrs:
                f.write(getattr(new, attr))
                f.write('\n')


def read_news_from_txt(txt_file) -> pd.DataFrame:
    """
    Read news from a txt file. Expecting the following structure:
    first line: title
    second line: summary
    third line: body
    """
    attrs: List[str] = [attr for attr in News.__annotations__]
    data: Dict[str, List[str]] = {attr: [] for attr in attrs}

    with open(txt_file, 'r', encoding='utf-8') as f:
        for attr in attrs:
            data[attr].append(f.readline())
    return pd.DataFrame(data)


def save_news_to_csv(news: List[News], output_folder: str, file_name: str = '_consolidated_news.csv') -> None:
    """Save results to one, unique, csv file_name.csv"""
    output_file_name: str = format_output_name(output_folder=output_folder, title=file_name)
    logger.info(f'Saving results to: {output_file_name}')
    # Create a column per attribute (not special)
    cols: List[str] = [attr for attr in News.__annotations__]
    data_dict: Dict[str, List[str]] = {col: [] for col in cols}
    for n in news:
        for col in cols:
            data_dict[col].append(getattr(n, col))
    data_df = pd.DataFrame(data_dict)
    data_df.to_csv(output_file_name, index=False)


def read_news_from_csv(csv_file: str) -> pd.DataFrame:
    """Read data from csv file and return a dataframe"""
    logger.info(f'Reading data from: {csv_file}')
    return pd.read_csv(csv_file)


def save_data_to_pickle(data: pd.DataFrame, output_path: str, name: str = 'transform_df.pkl') -> None:
    """Save dataframe to pickle"""
    create_output_folder(output_path)
    o_path: str = os.path.join(output_path, name)
    logger.info(f'Saving data to: {o_path}')
    data.to_pickle(o_path)
