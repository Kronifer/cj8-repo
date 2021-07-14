"""Layout system."""

from __future__ import annotations

import typing as t

import env
import space
import util
from exceptions import TooManySelected


class TextWidgetEntry:
    """Selectable entries to be plugged into a TextWidget object."""

    def __init__(self, text: str, style: str = "normal", *, selectable: bool =
                 True, selected: bool = False, on_select_fn: t.Callable = lambda: None):
        self.text: str = text
        self.style: str = style
        self.selectable: bool = selectable
        self.selected: bool = selected and selectable
        self.on_select_fn: bool = on_select_fn

    def __len__(self):
        return len(self.text)

    def __str__(self):
        return ["", "> "][self.selected and self.selectable] + self.text


class TextWidget:
    """Widget with text entries.

    By default (maximize = True) the text_w object will try to fill a large
    portion of the screen, with padding of a few cells around the edges. If
    maximize is set to false the object will try to make a small box hugging the
    textual content.

    (Possible TODOs?) At the moment there's no support for scrolling through
    pages, so it's on the caller to make sure all entries fit on one screen.
    Each entry must also fit on one line.
    """

    def __init__(self, entries: t.List[TextWidgetEntry], maximize: bool = True, center_entries: bool = False):
        self.entries = entries
        self.maximize = maximize
        self.center_entries = center_entries
        ind = None
        for entry in self.entries:
            if ind is not None and entry.selected:  # Confirm is only one entry was made "selected"
                raise TooManySelected
            if entry.selected:
                ind = self.entries.index(entry)
        self.active_index = ind

    def make_window(self) -> Window:
        """Makes widget content into a Window."""
        # dimensions:

        # -8 b/c 2 cells for root and widget borders & 2 for padding on each side
        max_width: int = env.term_width - 8
        max_height: int = env.term_height - 8

        self.entry_lens: t.List[int] = [len(str(e)) for e in self.entries]

        self.widget_width: int = min(max(self.entry_lens), max_width)
        self.widget_height: int = len(self.entries)

        if self.maximize:
            self.widget_width = max(self.widget_width, max_width - 12)
            self.widget_height = max(self.widget_height, max_height - 12)

        # Window position
        or_y: int = ((env.term_height - self.widget_height + 1) // 2) - 1
        bot_y: int = or_y + self.widget_height + 1
        or_x: int = ((env.term_width - self.widget_width + 1) // 2) - 1
        bot_x: int = or_x + self.widget_width + 1

        data: t.List[t.List[str]] = [["[normal] [/normal]"] * (self.widget_width + 2)
                                     for _ in range(self.widget_height + 2)]
        pt: space.Point = space.Point(or_y + 1, or_x + 1)
        for i, e in enumerate(self.entries):
            txt: str = str(e)
            if self.center_entries:
                txt = txt.center(self.widget_width)
            txt_as_l: t.List[str] = [f"[{e.style}]{t}[/{e.style}]" for t in txt]
            for j, let in enumerate(txt_as_l):
                data[i + 1][j + 1] = let
            pt = space.Point(pt.y + 1, pt.x)
        return Window(space.Point(or_y, or_x), space.Point(bot_y, bot_x), data, True)

    def select(self, dir: int) -> None:
        """Selects another entry based on "direction"."""
        if dir == 1:  # Direction is downwards
            for entry in self.entries[self.active_index+1:]:
                if entry.selectable:  # If not selectable, look to go down further.
                    self.entries[self.active_index].selected = False  # Deselect previous entry
                    self.active_index = self.entries.index(entry)
                    self.entries[self.active_index].selected = True  # Select new entry
                    break
        else:  # Direction is upwards
            if self.active_index == 0:  # Stops if selected entry is first entry.
                return                  # Otherwise, it would go to last entry.
            for entry in self.entries[self.active_index-1::-1]:
                if entry.selectable:
                    self.entries[self.active_index].selected = False
                    self.active_index = self.entries.index(entry)
                    self.entries[self.active_index].selected = True
                    break

        # Note: Nothing would happen if all of the entries were not selectable


class Window:
    """Area to be displayed.

    Rectangular region of formatted strings to be pushed onto a screen and
    rendered. Strings should be ready to be printed as a single glyph by
    rich.print.
    """

    def __init__(self, origin: space.Point, bottom: space.Point, data: t.List[t.List[str]],
                 border: bool = False, border_style: str = "normal"):
        # NB the region includes both origin and bottom
        util.assert_(bottom >= origin)
        self.height: int = bottom.y - origin.y + 1
        self.width: int = bottom.x - origin.x + 1
        util.assert_(len(data) == self.height)
        util.assert_(len(data[0]) == self.width)
        # we'll assume all the rows are of the same length
        self.origin = origin
        self.bottom = bottom
        self.data = data
        # note that the border may obscure data at the edges of the region
        self.border = border
        self.border_style = border_style

    def __str__(self):
        """Print window info for debugging purposes."""
        return(f"Window. Or: {self.origin} Bot: {self.bottom} Data: {len(self.data)} by {len(self.data[0])} matrix")

    def render(self, rendered_already: t.List[t.List[bool]], sc: env.Screen) -> int:
        """Push the window's data to the appropriate location on a screen."""
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
