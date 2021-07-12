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

    def __init__(self, origin: space.Point, bottom: space.Point, data:
                 t.List[t.List[str]], border: bool = False, border_style: str = "normal"):
        util.assert_(bottom >= origin)
        self.height: int = bottom.y - origin.y + 1
        self.width: int = bottom.x - origin.x + 1
        util.assert_(len(data) == self.height)
        util.assert_(len(data[0]) == self.width)
        # we assume all the rows are of the same length
        self.origin = origin
        self.bottom = bottom
        self.data = data
        # note that the border may obscure data at the edges of the region
        self.border = border
        self.border_style = border_style

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

        if not self.border:
            return num_cells_rendered

        # a border isn't going to look good or make much sense if the region
        # is too small
        util.assert_(self.height > 2 and self.width > 2)
        # top
        for i in range(self.width):
            pt = space.Point(self.origin.y, i + self.origin.x)
            render_cell_to_screen(f"[{self.border_style}]─[/{self.border_style}]", pt, sc)
        # bottom
        for i in range(self.width):
            pt = space.Point(self.bottom.y, i + self.origin.x)
            render_cell_to_screen(f"[{self.border_style}]─[/{self.border_style}]", pt, sc)
        # left
        for i in range(self.height):
            pt = space.Point(self.origin.y + i, self.origin.x)
            render_cell_to_screen(f"[{self.border_style}]│[/{self.border_style}]", pt, sc)
        # right
        for i in range(self.height):
            pt = space.Point(self.origin.y + i, self.bottom.x)
            render_cell_to_screen(f"[{self.border_style}]│[/{self.border_style}]", pt, sc)
        # corners
        render_cell_to_screen(f"[{self.border_style}]┌[/{self.border_style}]",
                              self.origin, sc)
        render_cell_to_screen(f"[{self.border_style}]┘[/{self.border_style}]",
                              self.bottom, sc)
        render_cell_to_screen(f"[{self.border_style}]┐[/{self.border_style}]",
                              space.Point(self.origin.y, self.bottom.x), sc)
        render_cell_to_screen(f"[{self.border_style}]└[/{self.border_style}]",
                              space.Point(self.bottom.y, self.origin.x), sc)

        return num_cells_rendered


def render_cell_to_screen(cell_str: str, p: space.Point, sc: env.Screen) -> None:
    """Push a cell's glyph to a screen."""
    y, x = p
    sc[y][x] = cell_str
