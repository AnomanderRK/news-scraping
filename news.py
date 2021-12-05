"""Simple notice object"""

from dataclasses import dataclass


@dataclass
class News:
    """Simple structure to store news from a site"""
    title: str
    summary: str
    body: str
