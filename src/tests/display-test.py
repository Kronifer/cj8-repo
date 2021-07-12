"""Test display code.

Run this manually since this needs visual inspection and uses input() to halt
for inspection.
"""

import unittest

import main
import space
import ui
import window


class TestDisplay(unittest.TestCase):
    """Test the display."""

    def test_display(self) -> None:
        """Main function to test the display."""
        if main.term.height < 24 or main.term.width < 80:
            print("Terminal must be at least 80x24, aborting.")
            quit()
        main.term.clear()
        with main.term.fullscreen(), main.term.cbreak(), main.term.hidden_cursor():

            root_data = [["[red]0[/red]"] * 80 for _ in range(24)]
            child_data = [["[blue]1[/blue]"] * 11 for _ in range(5)]

            root_panel: ui.Panel = ui.Panel(space.Point(0, 0), space.Point(23, 79), root_data)
            child_panel: ui.Panel = ui.Panel(space.Point(10, 5), space.Point(14, 15),
                                             child_data)

            window.panel_stack = [root_panel, child_panel]
            window.render()
            input()
            window.render()
            input()
            root_data[0][0] = "[blue]0[/blue]"
            window.render()
            input()
            root_data[0] = ["[blue]0[/blue]"] * main.term.width
            window.render()
            input()
