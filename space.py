"""General spatial constructs (points, regions, etc.)."""

import collections

Point = collections.namedtuple("Point", ("y", "x"))
"""A point in space."""


def offset_to_point_in_region(origin: Point, bottom: Point, offset: int) -> Point:
    """Given a region and offset, get point that far into the region."""
    or_y, or_x = origin
    bot_y, bot_x = bottom
    width = bot_x - or_x + 1
    return Point(or_y + offset // width, or_x + offset % width)


def area(a: Point, b: Point) -> int:
    """Return number of points in a region."""
    a_y, a_x = a
    b_y, b_x = b
    width = b_x - a_x + 1
    height = b_y - a_y + 1
    return width * height
