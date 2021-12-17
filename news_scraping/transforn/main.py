"""
Transform data to have more information regarding the news
"""

import argparse
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

# load data from config output
# Data wrangling
#   Add news identifier from folder structure (el universal, elpais, etc)
#   Add unique id using hashlib
#   Add host using urllib urlparse
#   Handle missing values
#   Handle duplicated values
# Data enrichment
#   use nlt to analyze natural language


def run(input_path: str) -> None:
    """Perform Data wrangling and enrichment"""
    pass


if __name__ == '__main__':
    # load the configuration file
    args_parser = argparse.ArgumentParser()
    # if no input path provided it will take the path from config
    args_parser.add_argument('--inputs', help='Path to input folder', required=False)
    args = args_parser.parse_args()
    input_f: str = args.inputs
    logger.info(f'Reading inputs from: {input_f}')
    run(input_f)
