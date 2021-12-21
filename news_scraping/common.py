"""Add useful common functions for different parts of the code"""
from __future__ import annotations      # resolve circular dependency with hints
import yaml
from typing import Dict, Union
from typing_extensions import TypedDict
from dataclasses import dataclass
import bs4
import os

from news_scraping.extract import news_parser as par
from news_scraping.output import create_output_folder


class SiteHint(TypedDict):
    """Hinting for config sites"""
    parser: str
    url: str
    queries: Dict[str, str]


Sites = Dict[str, Union[str, Dict[str, SiteHint]]]


def select_query(query: str, target: bs4.BeautifulSoup) -> bs4.ResultSet:
    """Apply query to target site and return matches"""
    return target.select(query)


def get_parser(parser_name: str) -> par.NewsParser:
    """map parser name to NewsParser class"""
    # noinspection PyTypeChecker
    parser_map: Dict[str, par.NewsParser] = dict(eluniversalparser=par.ElUniversalParser())
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
            self.config: Sites = yaml.load(config_file, yaml.FullLoader)

        # get a list of configs
        self._sites: Dict[str, Site] = self._get_sites()
        self._output_path: str = self._get_output_path()

    def _get_output_path(self) -> str:
        """Get output path from config"""
        config_output_path: Union[str, Dict[str, SiteHint]] = self.config['output_path']
        output_path: str = os.path.join(os.getcwd(), str(config_output_path))
        # Ensure path is available
        return create_output_folder(output_path)

    def _get_sites(self) -> Dict[str, Site]:
        """Get sites from config yaml"""
        sites: Union[str, Dict[str, SiteHint]] = self.config['news_sites']
        if not isinstance(sites, dict):
            raise TypeError(f'Invalid type: {sites}')
        return {name: Site(name,
                           attrs['url'],
                           attrs['queries'],
                           get_parser(attrs['parser']))
                for name, attrs in sites.items()}

    @property
    def sites(self) -> Dict[str, Site]:
        """Get sites from configuration"""
        return self._sites

    @property
    def output_folder(self) -> str:
        """Get output folder from config"""
        return self._output_path
