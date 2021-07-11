import typing as t

import blessed as b

term = b.Terminal()
TERM_HEIGHT = term.height
TERM_WIDTH = term.width
term = term


def assert_(testCond: t.bool) -> None:
    """Custom asset function."""
    if not testCond:
        raise AssertionError
