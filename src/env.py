"""Holds globals."""


import typing as t

import blessed

term: blessed.Terminal = blessed.Terminal()
term_height: int = term.height
term_width: int = term.width

# TYPES

Screen = t.List[t.List[str]]
