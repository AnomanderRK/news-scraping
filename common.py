"""Add useful common functions for different parts of the code"""
from __future__ import annotations      # resolve circular dependency with hints
import yaml
from typing import List, Dict, Union
from dataclasses import dataclass
import bs4

import news_parser as par


def select_query(query: str, target: bs4.BeautifulSoup) -> bs4.ResultSet:
    """Apply query to target site and return matches"""
    return target.select(query)


def get_parser(parser_name: str) -> par.NewsParser:
    """map parser name to NewsParser class"""
    # noinspection PyTypeChecker
    parser_map: Dict[str, par.NewsParser] = dict(eluniversalparser=par.ElUniversalParser(),
                                                 elpaisparser=par.ElPaisParser())
    return parser_map[parser_name.lower()]


@dataclass
class Site:
    """Store data for specific site"""
    name: str
    url: str
    queries: Dict[str, str]
    parser: par.NewsParser

    @property
    def homepage_links_query(self) -> str:
        """Get news links from homepage"""
        return self.queries['homepage_article_links']


class Config:
    def __init__(self, config_path: str = 'config.yaml'):
        """Load configuration from yaml"""
        self.config_path: str = config_path
        with open(self.config_path, 'r') as config_file:
            self.config: dict = yaml.load(config_file, yaml.FullLoader)

        # get a list of configs
        self._sites: Dict[str, Site] = self._get_sites()

    def _get_sites(self) -> Dict[str, Site]:
        """Get sites from config yaml"""
        sites: Dict = self.config['news_sites']
        return {name: Site(name,
                           attrs['url'],
                           attrs['queries'],
                           get_parser(attrs['parser']))
                for name, attrs in sites.items()}

    @property
    def sites(self) -> Dict[str, Site]:
        """Get sites from configuration"""
        return self._sites



