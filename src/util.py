"""Utility functions."""


def assert_(testCond: bool) -> None:
    """Custom asset function."""
    if not testCond:
        raise AssertionError
