# Name: main.py
# Purpose: Runs the main engine of the game
# Authors: @grivera64 and @Kronifer
# Date: July 2021
#


import time
import typing as t

import blessed as b

import env
import window

# constants
FRAMES_PER_SECOND = 60
SECONDS_PER_FRAME = FRAMES_PER_SECOND ** -1

key_to_action: dict[str, t.Callable] = {"KEY_LEFT": env.you.move_left,
                                        "KEY_RIGHT": env.you.move_right,
                                        "KEY_SPACE": env.you.jump,
                                        "KEY_ESCAPE": window.show_main_menu}


def update_world() -> None:
    """Point of entry for updating the simulation."""
    pass


def main() -> None:
    """The driver function of the Game

    :return: None
    """
    # Setup
    if env.term.height < 24 or env.term.width < 80:
        print("Terminal must be at least 80x24, aborting.")
        quit()
    env.term.clear()

    # Main Game loop conditionals
    game_over = False
    start_time, end_time = 0.0, 0.0

    # Main Game Loop
    with env.term.fullscreen(), env.term.cbreak(), env.term.hidden_cursor():
        while not game_over:

            # Getting start time of execution
            start_time = time.time()

            # Render the world/the main menu/whatever
            window.display()

            # Get and process input
            inp: b.keyboard.Keystroke = env.term.inkey(timeout=0)  # timeout=0 doesn't block
            inp_s = str(inp)

            if env.paused:  # the "simulation" should not tick
                window.process_input(inp_s)

            # Player acts and world updates
            else:
                if inp_s in key_to_action:
                    key_to_action[str(inp_s)]()
                if not env.paused:
                    update_world()

            # Check to see if the current frame has been shown for enough time to maintain
            # the current amount of frames per second
            end_time = time.time()
            if (time_passed := end_time - start_time) < SECONDS_PER_FRAME - 0.0001:
                time.sleep(SECONDS_PER_FRAME - time_passed)


# Run contents if file is the driver file
if __name__ == "__main__":
    main()
