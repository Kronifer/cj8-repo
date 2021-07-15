"""The entry point and controller for display code.

Elements in the game world or in the user interface construct windows (see
window.py), matrixes of information about what they want to show in a region
they own. This module composites them into a single image and then uses the
blessed library to print that image to the terminal screen each frame.

This module also contains functions controlling window interaction and
organization, e.g., passing input to interactive menus and popping up and
dismissing submenus.

"""

import typing as t

import rich

import env
import space
import util
import window

win_stack: t.List[window.Window] = []
input_sink_stack: t.List[t.Any] = []  # TODO? more correct to have List[OverarchingWidgetClass] here


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


def unpause() -> None:
    """Toggle unpausing of game."""
    env.paused = False


def end_game() -> None:
    """Stop main game loop."""
    env.game_over = True


main_menu: window.Menu = window.Menu([window.MenuEntry("Play", "blue",
                                      True, unpause),
                                      window.MenuEntry("Save Game", "blue"),
                                      window.MenuEntry("Load Game", "blue"),
                                      window.MenuEntry("Options", "blue"),
                                      window.MenuEntry("See highscores", "blue"),
                                      window.MenuEntry("Quit", "blue",
                                                       True, end_game)],
                                     maximize=False, center_entries=True)


input_sink_stack.append(main_menu)  # start with this open


def process_input(keypress: str) -> None:
    """Receive input to pass to a menu or interface object.

    TODO: this needs to do the part that's not just passing input on, too!
    """
    util.assert_(len(input_sink_stack) > 0)
    if keypress == "KEY_ESCAPE":
        input_sink_stack.pop()
        if len(input_sink_stack) == 0:
            unpause()
    else:
        input_sink_stack[-1].process_input(keypress)


def display(world: list) -> None or list:
    """Entry point into displaying on the terminal screen."""
    global win_stack
    if env.paused:  # Menu displayer
        main_menu_window = main_menu.make_window()
        win_stack.append(main_menu_window)
    else:  # Game displayer
        root_window = window.Window.from_origin(space.Point(0, 0), util.convert_data(world))
        win_stack = [root_window]
    render()
    return world if 'world' in locals() else None
