import pytest

import os
import news_scraping.io as store


@pytest.fixture
def valid_output_names():
    """valid output names"""
    return ['some_name', '_', 'some_simple_title',
            'max_len_title_available_is_50_chars_so_i_need_more']


@pytest.fixture
def output_names():
    """valid output names. list of tuples observed name, expected after transformation"""
    return [('some_symbols_fi:l*ep"a?t>h|<', 'some_symbols_filepath'),
            ('some spaces ', 'some_spaces'),
            ('max_len_title_available_is_50_chars_so_i_need_more_a',
             'max_len_title_available_is_50_chars_so_i_need_more')]


@pytest.fixture
def valid_output_dirs():
    """Get valid output dir names"""
    valid_dirs = [os.path.dirname(os.path.realpath(__file__))]
    return valid_dirs


@pytest.fixture
def valid_identifiers():
    """Get valid identifiers for output path"""
    return [1, "1"]


def test_format_output_name_valid(valid_output_dirs, valid_identifiers, valid_output_names):
    """Test func format output name when it receives valid path"""
    for valid_dir in valid_output_dirs:
        for valid_identifier in valid_identifiers:
            for valid_name in valid_output_names:
                # Since it is a valid output path, it should return the same as passed
                expected_path = os.path.join(valid_dir, f"{valid_identifier}_{valid_name}")
                observed_path = store.format_output_name(valid_dir, valid_name, valid_identifier)
                assert expected_path == observed_path


def test_format_output_name_invalid_output_name(valid_output_dirs, valid_identifiers, output_names):
    """Test function when it receives invalid output_names"""
    for valid_dir in valid_output_dirs:
        for valid_identifier in valid_identifiers:
            for invalid_name, valid_name in output_names:
                # Since it is a valid output path, it should return the same as passed
                expected_path = os.path.join(valid_dir, f"{valid_identifier}_{valid_name}")
                observed_path = store.format_output_name(valid_dir, invalid_name, valid_identifier)
                assert expected_path == observed_path
