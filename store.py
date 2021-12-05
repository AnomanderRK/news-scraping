"""methods to save results"""

import os
import datetime

from typing import List
from news import News


def create_output_folder(site: str) -> str:
    """Create output folder for site, if it does not exists and return it"""
    today: str = datetime.date.today().strftime('%d-%m-%Y')
    o_folder: str = os.path.join(os.getcwd(), today, site)
    if not os.path.isdir(o_folder):
        os.mkdir(o_folder)
    return o_folder


def save_news_to_folder(news: List[News], output_folder: str):
    """Save results into output folder"""
    for new in news:
        with open(f'{output_folder}/{new.title}.txt', 'w', encoding='utf-8') as f:
            # write the news
            f.write(new.title)
            f.write('\n\n')
            f.write('\n\n')
            f.write(f'{new.summary}')
            f.write('\n\n')
            f.write(f'{new.body}')
            f.write('\n\n')
