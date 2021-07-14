"""The entry point and controller for display code.

Elements in the game world or in the user interface construct windows (see
window.py), matrixes of information about what they want to show in a region
they own. This module composites them into a single image and then uses the
blessed library to print that image to the terminal screen each frame.

This module also contains functions controlling window interaction and
organization, e.g., passing input to interactive menus and popping up and
dismissing submenus.

"""

import pickle
import typing as t

import rich

import env
import space
import util
import window

win_stack: t.List[window.Window] = []


def render() -> None:
    """Composite live windows to a screen."""
    screen_to_render: env.Screen = [[" "] * env.term_width for _ in range(env.term_height)]
    num_of_cells_to_render: int = env.term_height * env.term_width
    rendered: t.List[t.List[bool]] = [[False] * env.term_width for _ in range(env.term_height)]
    for p in reversed(win_stack):
        num_of_cells_to_render -= p.render(rendered, screen_to_render)
        if num_of_cells_to_render <= 0:
            break
    print_screen(screen_to_render)


def print_screen(screen_to_render: env.Screen) -> None:
    """Print a screen on terminal."""
    with env.term.location(0, 0):
        rich.print("\n".join(["".join(i) for i in screen_to_render]))


def show_main_menu() -> None:
    """Pause game when the player hits Esc at game world."""
    env.paused = True


main_menu: window.TextWidget = window.TextWidget([window.TextWidgetEntry("Play", "bold blue", selected=True),
                                                  window.TextWidgetEntry("Save Game", "bold blue"),
                                                  window.TextWidgetEntry("Load Game", "bold blue"),
                                                  window.TextWidgetEntry("Options", "bold blue"),
                                                  window.TextWidgetEntry("See highscores", "bold blue"),
                                                  window.TextWidgetEntry("Quit", "bold blue")],
                                                 maximize=False, center_entries=True)


def process_input(keypress: str) -> None:
    """Receive input to pass to a menu or interface object."""
    if keypress == "KEY_UP":
        main_menu.select(-1)
    if keypress == "KEY_DOWN":
        main_menu.select(1)
    if keypress == "KEY_ENTER":
        active_entry = main_menu.entries[main_menu.active_index]
        if active_entry.text == "Quit":
            quit()
        if active_entry.text == "Play":
            env.paused = False


def display() -> None:
    """Entry point into displaying on the terminal screen."""
    global win_stack
    if env.paused:  # Menu displayer
        main_menu_window = main_menu.make_window()
        win_stack = [main_menu_window]
    else:  # Game displayer
        with open('tests/save.level', 'rb') as f:      # FILLER DATA
            level_data = pickle.load(f)  # noqa: S301
        root_window = window.Window(
            space.Point(0, 0),
            space.Point(len(level_data)-1, len(level_data[0])-1),
            util.convert_data(level_data)
        )
        win_stack = [root_window]
    render()
