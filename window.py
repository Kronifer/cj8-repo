"""This is a module-as-singleton controlling the panels. Works with ui.py."""

import typing as t

import rich

import main
import ui

# types
Screen = t.List[t.List[str]]


panel_stack: t.List[ui.Panel] = []

screen0: Screen = [[""] * main.TERM_WIDTH for _ in range(main.TERM_HEIGHT)]
screen1: Screen = [[""] * main.TERM_WIDTH for _ in range(main.TERM_HEIGHT)]
screen_to_render: Screen = screen0


def render() -> None:
    """Composite live panels to a screen."""
    global screen_to_render

    num_of_cells_to_render: int = main.TERM_HEIGHT * main.TERM_WIDTH
    rendered: t.List[t.List[bool]] = [[False] * main.TERM_WIDTH for _ in range(main.TERM_HEIGHT)]
    for p in reversed(panel_stack):
        num_of_cells_to_render -= p.render(rendered, screen_to_render)
        if num_of_cells_to_render <= 0:
            break
    print_screen(screen_to_render)

    screen_to_render = screen0 if screen_to_render == screen1 else screen1


def print_screen(screen_to_render: Screen) -> None:
    """Print a screen on terminal."""
    old_screen = screen0 if screen_to_render == screen1 else screen1
    for i in range(main.TERM_HEIGHT):
        for j in range(main.TERM_WIDTH):
            with main.term.location(j, i):  # NB blessed uses x, y
                if screen_to_render[i][j] != old_screen[i][j]:
                    rich.print(screen_to_render[i][j])
