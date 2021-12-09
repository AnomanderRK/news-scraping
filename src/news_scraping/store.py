"""methods to save results"""

import os
import datetime
import logging
from pathvalidate import sanitize_filepath

from typing import List, Union
from src.news_scraping.news import News

logger = logging.getLogger(__name__)


def create_output_folder(site: str) -> str:
    """Create output folder for site, if it does not exists and return it"""
    today: str = datetime.date.today().strftime('%d-%m-%Y')
    o_folder: str = os.path.join(os.getcwd(), today, site)
    if not os.path.isdir(o_folder):
        os.makedirs(o_folder)
    return o_folder


def format_output_name(output_folder: str, title: str, identifier: Union[int, str]) -> str:
    """format output name in he following way: output_folder/tile/identifier"""
    clean_title = title.strip().replace(' ', '_').replace("'", '"').title()
    clean_title = sanitize_filepath(clean_title, max_len=50)
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

    logger.info(f'Saving results finished!')

