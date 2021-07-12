"""Utility functions."""

import typing as t

KEY = {
    '': ' ',
    'AIR': ' ',
    'WATER': '[blue]█[/blue]',
    'GRASS': '[green]█[/green]',
    'LAVA': '[red]█[/red]',
    'ROCK': '[grey39]█[/grey39]',
}


def assert_(testCond: bool) -> None:
    """Custom asset function."""
    if not testCond:
        raise AssertionError


def convert_data(data: t.List[t.List[str]]) -> t.List[t.List[str]]:
    """Converts level creator data."""
    return [[KEY[col.upper()] for col in row] for row in data]
