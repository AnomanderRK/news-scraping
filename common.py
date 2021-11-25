"""Add useful common functions for different parts of the code"""

import yaml
from typing import List


class Config:
    def __init__(self, config_path: str = 'config.yaml'):
        """Load configuration from yaml"""
        self.config_path: str = config_path
        with open(self.config_path, 'r') as config_file:
            self.config: dict = yaml.load(config_file, yaml.FullLoader)

    @property
    def sites(self) -> List[str]:
        """Get sites from configuration"""
        return list(self.config['news_sites'].keys())

