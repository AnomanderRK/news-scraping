"""methods to save results"""

import os
import datetime

from typing import List
from news import News


def create_output_folder() -> str:
    """Create output folder if not exists and return it"""
    today: str = datetime.date.today().strftime('%d-%m-%Y')
    if not os.path.isdir(today):
        os.mkdir(today)
    return today


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
