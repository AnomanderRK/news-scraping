import pytest

import os
import news_scraping.store as store


@pytest.fixture
def valid_output_names():
    """valid output names"""
    return ['some_name', '_', 'some_simple_title',
            'max_len_title_available_is_50_chars_so_i_need_more']


@pytest.fixture
def valid_output_dirs():
    """Get valid output dir names"""
    valid_dirs = [os.path.dirname(os.path.realpath(__file__))]
    return valid_dirs


@pytest.fixture
def valid_identifiers():
    """Get valid identifiers for output path"""
    return [1, "1"]


def test_valid_format_output_name(valid_output_dirs, valid_identifiers, valid_output_names):
    """Test func format output name when it receives valid path"""
    for valid_dir in valid_output_dirs:
        for valid_identifier in valid_identifiers:
            for valid_name in valid_output_names:
                # Since it is a valid output path, it should return the same as passed
                expected_path = os.path.join(valid_dir, f"{valid_identifier}_{valid_name}")
                observed_path = store.format_output_name(valid_dir, valid_name, valid_identifier)
                assert expected_path == observed_path
