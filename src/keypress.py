# Name: keypress.py
# Purpose: Manages input for the game
# Author: @grivera64
# Date: July 2021


import blessed


class Trigger:
    """Represents a trigger"""

    def __init__(self, wait_time: int = 0):
        """Creates a Trigger object

        :param wait_time: (Optional) Set a wait time
        for self.get_input()
        """
        self.wait_time = wait_time

        # Create a terminal instance
        self.term = blessed.Terminal()
        pass

    def set_wait_time(self, wait_time: int) -> None:
        """Sets wait_time to a new value

        :param wait_time: The amount of time
        to wait in get_input
        :return: None
        """
        self.wait_time = wait_time
        pass

    def get_input(self) -> blessed.keyboard.Keystroke:
        """Checks for any input at intervals

        :return: KeyStroke a unicode representation
        of scanned key
        """
        with self.term.cbreak():

            current_key = self.term.inkey(timeout=self.wait_time)

        return None if not current_key else current_key
