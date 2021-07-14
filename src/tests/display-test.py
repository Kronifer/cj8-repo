"""Test display code.

Run this manually since this needs visual inspection and uses time.sleep(2) to halt
for inspection.
"""


import pickle
import time
import typing as t
import unittest

import display
import env
import space
import util
import window


class TestDisplay(unittest.TestCase):
    """Test the display."""

    def run(self, result: t.Optional[unittest.TestResult] = None) -> t.Optional[unittest.TestResult]:
        """Override built-in run so tests are run in an appropriate context."""
        if env.term.height < 24 or env.term.width < 80:
            print("Terminal must be at least 80x24, aborting.")
            quit()
        env.term.clear()
        with env.term.fullscreen(), env.term.cbreak(), env.term.hidden_cursor():
            return super(TestDisplay, self).run(result)

    def test_display(self) -> None:
        """Test basic Display and Window features."""
        root_data = [["[red]0[/red]"] * 80 for _ in range(24)]
        child_data = [["[blue]1[/blue]"] * 11 for _ in range(5)]

        root_window: window.Window = window.Window(space.Point(0, 0), space.Point(23, 79), root_data)
        child_window: window.Window = window.Window(space.Point(10, 5), space.Point(14, 15),
                                                    child_data, border_style="green", border=True)

        display.win_stack = [root_window, child_window]
        display.render()
        time.sleep(2)
        root_data[0][0] = "[blue]0[/blue]"
        display.render()
        time.sleep(2)
        root_data[0] = ["[blue]0[/blue]"] * env.term.width
        display.render()
        time.sleep(2)

    def test_converter(self) -> None:
        """Test for displaying level saves."""
        with open('tests/save.level', 'rb') as f:
            data = pickle.load(f)  # noqa: S301

        rock_data = [
            ['AIR', 'AIR', 'AIR'],
            ['AIR', 'AIR', 'AIR'],
            ['AIR', 'AIR', 'AIR'],
            ['AIR', 'AIR', 'AIR'],
            ['AIR', 'AIR', 'AIR'],
            ['AIR', 'AIR', 'AIR'],
            ['AIR', 'AIR', 'AIR'],
            ['AIR', 'AIR', 'AIR'],
            ['AIR', 'AIR', 'AIR'],
            ['GRASS', 'AIR', 'AIR', 'GRASS'],
            ['ROCK', 'WATER', 'WATER', 'ROCK'],
            ['ROCK', 'WATER', 'WATER', 'ROCK'],
            ['ROCK', 'WATER', 'WATER', 'ROCK'],
            ['ROCK', 'ROCK', 'ROCK', 'ROCK'],
        ]

        root_data = util.convert_data(data)
        rock_data = util.convert_data(rock_data)

        root_window: window.Window = window.Window(space.Point(0, 0), space.Point(len(root_data) - 1,
                                                                                  len(root_data[0]) - 1), root_data)
        rock_window: window.Window = window.Window(space.Point(0, len(root_data[0]) + 4),
                                                   space.Point(len(rock_data) - 1,
                                                               len(root_data[0]) + 4 + len(rock_data[0]) - 1),
                                                   rock_data)

        display.win_stack = [root_window, rock_window]
        display.render()
        time.sleep(2)

    def test_text_widgets(self) -> None:
        """Test text widgets."""
        text_w: window.TextWidget = window.TextWidget([window.TextWidgetEntry("foo"),
                                                       window.TextWidgetEntry("bar"),
                                                       window.TextWidgetEntry("baz"),
                                                       window.TextWidgetEntry("quuuuuuuux")],
                                                      center_entries=True)
        text_w_window = text_w.make_window()
        display.win_stack = [text_w_window]
        display.render()
        time.sleep(2)
        root_data = [["[red]0[/red]"] * 80 for _ in range(24)]
        root_window: window.Window = window.Window(space.Point(0, 0), space.Point(len(root_data) - 1,
                                                                                  len(root_data[0]) - 1), root_data)
        text_w.maximize = False
        text_w.center_entries = False
        text_w_window = text_w.make_window()
        display.win_stack = [root_window, text_w_window]
        display.render()
        time.sleep(2)

    def test_menu(self) -> None:
        """Test the menu and keypresses."""
        baz_callback: t.Callable = lambda: "baz's callback"
        bar_callback: t.Callable = lambda: "bar's awesome callback"
        text_w: window.TextWidget = window.TextWidget([window.TextWidgetEntry("foo", selected=True),
                                                       window.TextWidgetEntry("bar", on_select_fn=bar_callback),
                                                       window.TextWidgetEntry("baz", on_select_fn=baz_callback),
                                                       window.TextWidgetEntry("quuuuuuuux")],
                                                      center_entries=True)

        while True:
            text_w_window = text_w.make_window()
            display.win_stack = [text_w_window]
            display.render()

            inp = env.term.inkey()
            if inp.name == "KEY_DOWN":
                text_w.select(1)
            if inp.name == "KEY_UP":
                text_w.select(-1)
            if inp.name in ("KEY_ESCAPE", "KEY_ENTER"):
                break

        selected_entry = text_w.entries[text_w.active_index]

        data: str = [f"The last selected entry was '{selected_entry.text}'. You escaped the test using '{inp.name}'.",
                     "The callback's return was \"{selected_entry.on_select_fn()}\""]
        text_w: window.TextWidget = window.TextWidget([window.TextWidgetEntry(data[0], selectable=False),
                                                       window.TextWidgetEntry(data[1], selectable=False)],
                                                      center_entries=True)
        display.win_stack = [text_w.make_window()]
        display.render()
        time.sleep(4)
