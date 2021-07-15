"""Layout system."""

from __future__ import annotations

import typing as t

import env
import space
import util


class TextWidgetEntry:
    """Text entries to be plugged into a TextWidget object."""

    def __init__(self, text: str, style: str = "normal"):
        self.text: str = text
        self.style: str = style

    def __len__(self):
        return len(self.text)

    def __str__(self):
        return self.text


class MenuEntry(TextWidgetEntry):
    """Selectable text entries to be plugged into a Menu object."""

    def __init__(self, text: str, style: str = "normal", selectable: bool =
                 True, on_select_fn: t.Callable = lambda: None):
        self.selectable = selectable
        self.on_select_fn = on_select_fn
        TextWidgetEntry.__init__(self, text, style)


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

    def get_text_as_list(self, i: int, e: TextWidgetEntry, txt: str, style: str, centered: bool) -> t.List[str]:
        """Actually construct the entry text as a row of cells.

        Pulled out so Menu can override and print selected entries differently.
        """
        # assert out if a small but legal terminal width would cause an index
        # error when we try to write the list into data
        util.assert_(len(e) <= self.data_width)  # NB after "> " might be added
        if centered:
            txt = txt.center(self.data_width)
        return [f"[{e.style}]{t}[/{e.style}]" for t in txt]

    def make_window(self) -> Window:
        """Makes widget content into a Window."""
        # -8 b/c 2 cells for root and widget borders & 2 for padding on each side
        max_width: int = env.term_width - 8
        max_height: int = env.term_height - 8

        self.entry_lens: t.List[int] = [len(str(e)) for e in self.entries]
        #  hack: +2 is space for the "> " on selected entries
        self.data_width: int = min(max(self.entry_lens), max_width) + 2
        self.data_height: int = len(self.entries)

        if self.maximize:
            self.data_width = max(self.data_width, max_width - 12)
            self.data_height = max(self.data_height, max_height - 12)

        # Window position
        self.or_y: int = ((env.term_height - self.data_height + 1) // 2) - 1
        self.bot_y: int = self.or_y + self.data_height + 1
        self.or_x: int = ((env.term_width - self.data_width + 1) // 2) - 1
        self.bot_x: int = self.or_x + self.data_width + 1

        data: t.List[t.List[str]] = [["[normal] [/normal]"] * (self.data_width + 2)
                                     for _ in range(self.data_height + 2)]
        pt: space.Point = space.Point(self.or_y + 1, self.or_x + 1)
        for i, e in enumerate(self.entries):
            txt_as_l = self.get_text_as_list(i, e, e.text, e.style, self.center_entries)
            for j, let in enumerate(txt_as_l):
                data[i + 1][j + 1] = let
            pt = space.Point(pt.y + 1, pt.x)
        return Window(space.Point(self.or_y, self.or_x), space.Point(self.bot_y, self.bot_x), data, True)


class Menu(TextWidget):
    """TextWidget with selectable entries.

    Selection runs an associated function.
    """

    def __init__(self, entries: t.List[TextWidgetEntry], maximize: bool = True, center_entries: bool = False):
        TextWidget.__init__(self, entries, maximize, center_entries)
        self.selected_entry_idx = 0

    def get_text_as_list(self, i: int, e: MenuEntry, txt: str, style: str, centered: bool) -> t.List[str]:
        """Actually construct the entry text as a row of cells."""
        # assert out if a small but legal terminal width would cause an index
        # error when we try to write the list into data
        if i == self.selected_entry_idx:
            txt = "> " + txt
            style = "bold " + style if style == "normal" else "bold"
        return TextWidget.get_text_as_list(self, i, e, txt, style, centered)

    def process_input(self, cmd_name: str) -> None:
        """Process menu-specific input.

        TODO: less repetition between KEY_UP and KEY_DOWN
        """
        selectable_entries: t.List[t.Tuple[int, MenuEntry]]
        if cmd_name == "KEY_ENTER" or cmd_name == "KEY_SPACE":
            self.entries[self.selected_entry_idx].on_select_fn()
        elif cmd_name == "KEY_DOWN":
            selectable_es = filter(lambda t: t[1].selectable,
                                   list(enumerate(self.entries))[self.selected_entry_idx:])
            next(selectable_es)  # consume the current entry
            try:
                self.selected_entry_idx = next(selectable_es)[0]
            except StopIteration:
                pass  # do nothing if already on last selectable entry
        elif cmd_name == "KEY_UP":
            selectable_es = filter(lambda t: t[1].selectable,
                                   reversed(list(enumerate(self.entries))[:self.selected_entry_idx]))
            try:
                self.selected_entry_idx = next(selectable_es)[0]
            except StopIteration:
                pass

        #  ignore other inputs. Display handles Esc


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
