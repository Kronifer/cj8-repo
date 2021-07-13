"""Holds globals."""


import typing as t

import blessed

import player

term: blessed.Terminal = blessed.Terminal()
term_height: int = term.height
term_width: int = term.width

paused: bool = False

you: player.Player = player.Player()

# TYPES

Screen = t.List[t.List[str]]
