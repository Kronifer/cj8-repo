"""Utility functions."""

import typing as t

import env

KEY = {
    '': ' ',
    'AIR': ' ',
    'WATER': '[blue]█[/blue]',
    'GRASS': '[green]█[/green]',
    'LAVA': '[red]█[/red]',
    'ROCK': '[grey39]█[/grey39]',
    'PLAYER': '@',
    'SPIKE_UP': 'M',
    'SPIKE_DOWN': 'W'
}


def assert_(testCond: bool) -> None:
    """Custom asset function."""
    if not testCond:
        raise AssertionError


def dprint(to_print: str) -> None:
    """For debugging."""
    with env.term.location(80, 0):
        print(to_print)


def convert_data(data: t.List[t.List[str]]) -> t.List[t.List[str]]:
    """Converts level creator data."""
    return [[KEY[col.upper()] for col in row] for row in data]
