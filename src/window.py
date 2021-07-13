"""This is a module-as-singleton controlling the panels. Works with ui.py."""

import typing as t

import rich

import env
import ui

panel_stack: t.List[ui.Panel] = []


def clear_screen(sc: env.Screen) -> None:
    """Necessary to avoid artifacts in places without any panel."""
    for i, row in enumerate(sc):
        for j, col in enumerate(row):
            sc[i][j] = ""


def render() -> None:
    """Composite live panels to a screen."""
    screen_to_render: env.Screen = [[" "] * env.term_width for _ in range(env.term_height)]

    clear_screen(screen_to_render)
    num_of_cells_to_render: int = env.term_height * env.term_width
    rendered: t.List[t.List[bool]] = [[False] * env.term_width for _ in range(env.term_height)]
    for p in reversed(panel_stack):
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


main_menu: ui.Menu = ui.Menu([ui.MenuEntry("Play", "bold blue"),
                              ui.MenuEntry("Save Game", "bold blue"),
                              ui.MenuEntry("Load Game", "bold blue"),
                              ui.MenuEntry("Options", "bold blue"),
                              ui.MenuEntry("See highscores", "bold blue"),
                              ui.MenuEntry("Quit", "bold blue")],
                             center_entries=True)

main_menu_panel = main_menu.make_panel()


def process_input(keypress: str) -> None:
    """Receive input to pass to a menu or interface object."""
    pass


def display() -> None:
    """Entry point into displaying on the terminal screen."""
    global panel_stack
    panel_stack = [main_menu_panel]
    render()
