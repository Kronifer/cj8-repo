# Name: main.py
# Purpose: Runs the main engine of the game
# Authors: @grivera64 and @Kronifer
# Date: July 2021
#

import pickle
import time
import typing as t

import blessed as b

import display
import env
import player

# constants
FRAMES_PER_SECOND = 60
SECONDS_PER_FRAME = FRAMES_PER_SECOND ** -1
is_jumping = False


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
    inp_s = ""

    # Main Game loop conditionals
    game_over = False
    global is_jumping
    start_time, end_time = 0.0, 0.0
    env.paused = True  # Show menu first
    with open('tests/save.level', 'rb') as file:
        world = pickle.load(file)
    with open('tests/save.level', 'rb') as file:
        backupworld = pickle.load(file)

    # Main Game Loop
    with env.term.fullscreen(), env.term.cbreak(), env.term.hidden_cursor():
        while not game_over:
            keypress_copy = inp_s

            # Getting start time of execution
            start_time = time.time()

            # Render the world/the main menu/whatever
            world = display.display(world=world)
            you: player.Player = player.Player(world=world, backupworld=backupworld)
            key_to_action: dict[str, t.Callable] = {"KEY_LEFT": you.move_left,
                                                    "KEY_RIGHT": you.move_right,
                                                    "KEY_UP": you.jump,
                                                    "KEY_SPACE": you.jump,
                                                    "KEY_ESCAPE": display.show_main_menu}

            # Get and process input
            inp: b.keyboard.Keystroke = env.term.inkey(timeout=0.15)
            inp_s = inp.name
            if inp_s is None:
                for element in world:
                    worldindex = world.index(element)
                    try:
                        index = element.index("PLAYER")
                        break
                    except ValueError:
                        pass
                if world[worldindex + 1][index] in ["AIR", ""]:
                    you.move_down()

            if env.paused:  # the "simulation" should not tick
                display.process_input(inp_s)
            # Player acts and world updates
            else:
                if inp_s in key_to_action:
                    key_to_action[str(inp_s)]()
                if not env.paused:
                    update_world()
                if keypress_copy == inp_s and inp_s in ['KEY_UP', 'KEY_SPACE']:
                    you.move_down()

            # Check to see if the current frame has been shown for enough time to maintain
            # the current amount of frames per second
            end_time = time.time()
            if (time_passed := end_time - start_time) < SECONDS_PER_FRAME - 0.0001:
                time.sleep(SECONDS_PER_FRAME - time_passed)


# Run contents if file is the driver file
if __name__ == "__main__":
    main()
