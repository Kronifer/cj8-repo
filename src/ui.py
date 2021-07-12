"""Layout system."""

import typing as t

import env
import space
import util


class Panel:
    """Area to be displayed.

    Rectangular region of formatted strings to be pushed onto a screen and
    rendered. Strings should be ready to be printed as a single glyph by
    rich.print.
    """

    def __init__(self, origin: space.Point, bottom: space.Point, data: t.List[t.List[str]]):
        util.assert_(bottom >= origin)
        util.assert_(len(data) == bottom.y - origin.y + 1)
        util.assert_(len(data[0]) == bottom.x - origin.x + 1)
        # we assume all the rows are of the same length
        self.origin = origin
        self.bottom = bottom
        self.data = data

    def render(self, rendered_already: t.List[t.List[bool]], sc: env.Screen) -> int:
        """Push the Panel's data to the appropriate location on a screen."""
        num_cells_rendered = 0
        or_y, or_x = self.origin

        for i, j in enumerate(self.data):
            for k, m in enumerate(j):
                pt = space.Point(i + or_y, k + or_x)
                if rendered_already[pt.y][pt.x]:
                    continue
                render_cell_to_screen(m, pt, sc)
                rendered_already[pt.y][pt.x] = True
                num_cells_rendered += 1
        return num_cells_rendered


def render_cell_to_screen(cell_str: str, p: space.Point, sc: env.Screen) -> None:
    """Push a cell's glyph to a screen."""
    y, x = p
    sc[y][x] = cell_str
