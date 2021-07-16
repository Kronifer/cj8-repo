# Name: main.py
# Purpose: Runs the main engine of the game
# Authors: @grivera64 and @Kronifer
# Date: July 2021
#

import pickle
import time
import typing as t
from copy import deepcopy

import blessed as b

import display
import env
import player
import util

# constants
FRAMES_PER_SECOND = 60
SECONDS_PER_FRAME = FRAMES_PER_SECOND ** -1
is_jumping = False
levels = env.levels
world = levels[0]
backupworld = deepcopy(levels[0])

SOLIDS: list = ["GRASS", "FLOOR", "ROCK", "LAVA"]


def save() -> None:
    """Saves your progress."""
    global levels
    with open("saves/main.save", "wb") as f:
        pickle.dump(levels, f)


def load() -> None:
    """Loads the saved game."""
    global levels
    global world
    global backupworld
    try:
        with open("saves/main.save", "rb") as f:
            levels = pickle.load(f)
        world = levels[0]
        backupworld = deepcopy(levels[0])
        env.paused = False
    except EOFError:
        pass
    except FileNotFoundError:
        pass


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
    global levels
    # Main Game loop conditionals
    global is_jumping
    start_time, end_time = 0.0, 0.0
    env.paused = True  # Show menu first

    # Main Game Loop
    with env.term.fullscreen(), env.term.cbreak(), env.term.hidden_cursor():
        while not env.game_over:
            global world, backupworld
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
                                                    "KEY_ESCAPE": display.show_main_menu,
                                                    "KEY_DELETE": save,
                                                    "KEY_BACKSPACE": load}

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
                if world[worldindex + 1][index] in SOLIDS:
                    is_jumping = False
                else:
                    is_jumping = False
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
                        is_jumping = False
                        you.move_down()
                    if inp_s in ['KEY_UP', 'KEY_SPACE']:
                        is_jumping = True

            for element in world:
                worldindex = world.index(element)
                try:
                    index = element.index("PLAYER")
                    break
                except ValueError:
                    pass
            try:
                if world[worldindex + 1][index] in ["LAVA", "SPIKE_UP"]:
                    if is_jumping:
                        pass
                    else:
                        env.hits -= 1
            except IndexError:
                env.hits -= 1
            if env.hits > 4:
                if env.hits < env.previoushits:
                    world = deepcopy(backupworld)
                    env.previoushits = env.hits
            if env.hits == 4:
                util.KEY['PLAYER'] = 'X'
            if env.hits == 3:
                util.KEY['PLAYER'] = 'x'
            if env.hits == 2:
                util.KEY['PLAYER'] = '+'
            if env.hits == 1:
                util.KEY['PLAYER'] = '.'
            if env.hits == 0:
                env.game_over = True
            if backupworld[worldindex][index] == "PLAYER_END":
                levels.pop(0)
                if int(len(levels)) == 0:
                    env.game_over = True
                    break
                env.level_num += 1
                world = levels[0]
                backupworld = deepcopy(levels[0])

            # Check to see if the current frame has been shown for enough time to maintain
            # the current amount of frames per second
            end_time = time.time()
            if (time_passed := end_time - start_time) < SECONDS_PER_FRAME - 0.0001:
                time.sleep(SECONDS_PER_FRAME - time_passed)


# Run contents if file is the driver file
if __name__ == "__main__":
    main()
