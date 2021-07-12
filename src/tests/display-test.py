"""Test display code.

Run this manually since this needs visual inspection and uses time.sleep(2) to halt
for inspection.
"""


import pickle
import time
import unittest

import env
import space
import ui
import util
import window


class TestDisplay(unittest.TestCase):
    """Test the display."""

    def test_display(self) -> None:
        """Main function to test the display."""
        if env.term.height < 24 or env.term.width < 80:
            print("Terminal must be at least 80x24, aborting.")
            quit()
        env.term.clear()
        with env.term.fullscreen(), env.term.cbreak(), env.term.hidden_cursor():

            root_data = [["[red]0[/red]"] * 80 for _ in range(24)]
            child_data = [["[blue]1[/blue]"] * 11 for _ in range(5)]

            root_panel: ui.Panel = ui.Panel(space.Point(0, 0), space.Point(23, 79), root_data)
            child_panel: ui.Panel = ui.Panel(space.Point(10, 5), space.Point(14, 15),
                                             child_data, border_style="green", border=True)

            window.panel_stack = [root_panel, child_panel]
            window.render()
            time.sleep(2)
            window.render()
            time.sleep(2)
            root_data[0][0] = "[blue]0[/blue]"
            window.render()
            time.sleep(2)
            root_data[0] = ["[blue]0[/blue]"] * env.term.width
            window.render()
            time.sleep(2)

    def test_level_display(self) -> None:
        """Test for displaying level saves."""
        if env.term.height < 24 or env.term.width < 80:
            print("Terminal must be at least 80x24, aborting.")
            quit()
        env.term.clear()

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

        with env.term.fullscreen(), env.term.cbreak(), env.term.hidden_cursor():
            root_data = util.convert_data(data)
            rock_data = util.convert_data(rock_data)

            root_panel: ui.Panel = ui.Panel(space.Point(0, 0), space.Point(len(root_data) - 1,
                                            len(root_data[0]) - 1), root_data)
            rock_panel: ui.Panel = ui.Panel(space.Point(0, len(root_data[0]) + 4),
                                            space.Point(len(rock_data) - 1,
                                            len(root_data[0]) + 4 + len(rock_data[0]) - 1),
                                            rock_data)

            window.panel_stack = [root_panel, rock_panel]
            window.render()
            time.sleep(2)
