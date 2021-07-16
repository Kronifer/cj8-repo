"""Holds globals."""


import typing as t

import blessed

import level

term: blessed.Terminal = blessed.Terminal()
# some terminal emulators apparently don't deal well with our trying to use the
# full height, and bounce the screen around
term_height: int = term.height - 2
term_width: int = term.width
hits: int = 7
previoushits: int = 7

paused: bool = False
game_over: bool = False

levels: list = level.load_levels()
level_num: int = 1  # (Level #1)
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
