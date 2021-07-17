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
    'PLAYER': '☺',
    'PLAYER_END': '[light blue]◻[/light blue]',
    'SPIKE_UP': '[grey39]▲[/grey39]',
    'SPIKE_DOWN': '[grey39]▼[/grey39]'
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
    displaydata = []
    for row in data:
        subdata = []
        for col in row:
            try:
                if col == "":
                    col = "AIR"
                subdata.append(KEY[col.upper()])
            except KeyError:
                subdata.append(col.upper())
        displaydata.append(subdata)
    return displaydata
