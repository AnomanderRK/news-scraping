"""Add data to news dataframe"""
import pandas as pd
from nltk.corpus import stopwords
import nltk
import logging

logger = logging.getLogger(__name__)

# Download data needed for nltk analysis
nltk.download('punkt')
nltk.download('stopwords')

SPANISH_STOPWORDS = set(stopwords.words('spanish'))


def tokenize_column(news_df: pd.DataFrame, column_name: str) -> pd.Series:
    """Tokenize column using natural language toolkit"""
    try:
        s: pd.Series = (news_df
                        .dropna()
                        .apply(lambda row: nltk.word_tokenize(row[column_name]), axis=1)
                        .apply(lambda tokens: list(filter(lambda token: token.isalpha(), tokens)))
                        .apply(lambda tokens: list(map(lambda token: token.lower(), tokens)))  # type: ignore
                        .apply(lambda word_list: list(filter(lambda word: word not in SPANISH_STOPWORDS, word_list)))
                        .apply(lambda valid_word_list: len(valid_word_list)))
    except Exception as e:
        logger.error(e)
        s: pd.Series = pd.Series(len(news_df))
    print(s)
    return s
