"""Holds globals."""


import typing as t

import blessed

import level

term: blessed.Terminal = blessed.Terminal()
# some terminal emulators apparently don't deal well with our trying to use the
# full height, and bounce the screen around
term_height: int = term.height - 2
term_width: int = term.width
hits: int = 3
previoushits: int = 3

paused: bool = False
game_over: bool = False

levels: list = level.load_levels()
logo: str = """
██████╗  █████╗  ██████╗██╗  ██╗███████╗██████╗
██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗
██████╔╝███████║██║     █████╔╝ █████╗  ██║  ██║
██╔═══╝ ██╔══██║██║     ██╔═██╗ ██╔══╝  ██║  ██║
██║     ██║  ██║╚██████╗██║  ██╗███████╗██████╔╝
╚═╝     ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═════╝
"""


# TYPES

Screen = t.List[t.List[str]]
