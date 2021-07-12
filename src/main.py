# Name: main.py
# Purpose: Runs the main engine of the game
# Authors: @giode#1018 and @Kronifer#5647
# Date: July 2021
#


import time

import blessed as b

# constants
FRAMES_PER_SECOND = 60
SECONDS_PER_FRAME = FRAMES_PER_SECOND ** -1

# globals
term: b.Terminal = b.Terminal()
term_height: int = term.height
term_width: int = term.width


# utility functions
def assert_(testCond: bool) -> None:
    """Custom asset function."""
    if not testCond:
        raise AssertionError


def main() -> None:
    """The driver function of the Game

    :return: None
    """
    # Setup
    if term.height < 24 or term.width < 80:
        print("Terminal must be at least 80x24, aborting.")
        quit()
    term.clear()

    # Main Game loop conditionals
    game_over = False
    start_time, end_time = 0.0, 0.0
    counter = 1200

    # Main Game Loop
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
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


# Run contents if file is the driver file
if __name__ == "__main__":
    main()
