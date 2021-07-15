"""Holds globals."""


import typing as t

import blessed

term: blessed.Terminal = blessed.Terminal()
# some terminal emulators apparently don't deal well with our trying to use the
# full height, and bounce the screen around
term_height: int = term.height - 2
term_width: int = term.width
hits: int = 2
previoushits: int = 2

paused: bool = False
game_over: bool = False

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
