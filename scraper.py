"""
Get the news for today from 'la republica' and save them into [today] folder as different txt files
"""
import requests
import os
import datetime
import lxml.html as html

from typing import List

HOME_URL = 'https://www.larepublica.co/'
XPATH_LINK_TO_ARTICLE = '//text-fill/a[@class="economiaSect" or @class="empresasSect" or @class="ocioSect" ' \
                        'or @class="globoeconomiaSect" or @class="analistas-opinionSect"]/@href'
XPATH_TITTLE = '//div[@class="mb-auto"]/text-fill/span/text()'
XPATH_SUMMARY = '//div[@class="lead"]/p/text()'
XPATH_BODY = '//div[@class="html-content"]/p[not(@class)]/text()'


def parse_notice(link: str, output_folder: str) -> None:
    """
    Get notice from link and save it into today folder

    Parameters
    ----------
    link: str
        url to news
    output_folder: str
        folder path to store the news

    Returns
    -------
    None
    """
    try:
        response: requests.Response = requests.get(link)
        if response.status_code == 200:
            notice: str = response.content.decode('utf-8')
            parsed: html.HtmlElement = html.fromstring(notice)

            try:
                title: str = parsed.xpath(XPATH_TITTLE)[0]
                tile: str = title.replace('\"', '')
                summary: str = parsed.xpath(XPATH_SUMMARY)[0]
                body: list = parsed.xpath(XPATH_BODY)   # list of paragraphs
            except IndexError:
                print(f'No news from: {link}')
                return

            # save results
            with open(f'{output_folder}/{title}.txt', 'w', encoding='utf-8') as f:
                # write the news
                f.write(tile)
                f.write('\n\n')
                f.write('\n\n')
                f.write(f'{summary}')
                f.write('\n\n')
                for p in body:
                    f.write(f'{p}')
                    f.write('\n\n')

        else:
            raise ValueError(f'Error: {response.status_code} for {link}')
    except ValueError as ve:
        print(ve)
    pass


def parse_home() -> List[str]:
    """
    Extract news

    Returns
    -------
    list of news

    Raises
    ------
    ValueError
        if response from server is not OK
    """
    try:
        response: requests.Response = requests.get(HOME_URL)
        if response.status_code == 200:     # ok
            home: str = response.content.decode('utf-8')
            parsed: html.HtmlElement = html.fromstring(home)
            links_to_news: List[str] = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            return links_to_news
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)
    return list()


def create_output_folder() -> str:
    """Create output folder if not exists and return it"""
    today: str = datetime.date.today().strftime('%d-%m-%Y')
    if not os.path.isdir(today):
        os.mkdir(today)
    return today


def run():
    """Get the news for today and save them into [today] folder as different txt files"""
    output_folder: str = create_output_folder()
    today_news: List[str] = parse_home()
    for news in today_news:
        parse_notice(news, output_folder)


if __name__ == '__main__':
    run()
