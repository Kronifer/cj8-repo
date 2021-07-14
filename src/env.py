"""Holds globals."""


import typing as t

import blessed

import player

term: blessed.Terminal = blessed.Terminal()
# some terminal emulators apparently don't deal well with our trying to use the
# full height, and bounce the screen around
term_height: int = term.height - 2
term_width: int = term.width

paused: bool = False

you: player.Player = player.Player(world=["placeholder", "world"])

# TYPES

Screen = t.List[t.List[str]]
