<<<<<<< HEAD
#
# Name: main.py
# Purpose: Runs the main engine of the game
# Authors: @giode#1018 and @Kronifer#5647
# Date: July 2021
#

# imports
import time

# constants
FRAMES_PER_SECOND = 60
SECONDS_PER_FRAME = FRAMES_PER_SECOND ** -1


def main() -> None:
    """The driver function of the Game

    :return: None
    """
    # Main Game loop conditionals
    game_over = True
    start_time, end_time = 0, 0
    counter = 1200

    # Main Game Loop
    while not game_over:

        # Getting start time of execution
        start_time = time.time()

        # TODO: Update Screen

        # TODO: Draw to the screen

        # Check to see if the current frame has been shown for enough time to maintain
        # the current amount of frames per second
        end_time = time.time()
        if (time_passed := end_time - start_time) < SECONDS_PER_FRAME - 0.0001:

            time.sleep(SECONDS_PER_FRAME - time_passed)

        # Loop until counter is 0
        counter -= 1

        if counter < 1:

            game_over = True

    pass


# Run contents if file is the driver file
if __name__ == "__main__":

    main()
=======
import typing as t

import blessed as b

term = b.Terminal()
TERM_HEIGHT = term.height
TERM_WIDTH = term.width
term = term


def assert_(testCond: t.bool) -> None:
    """Custom asset function."""
    if not testCond:
        raise AssertionError
>>>>>>> 563231c (Fixed lint and moved .py files to src directory)
