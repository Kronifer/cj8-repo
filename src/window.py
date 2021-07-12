"""This is a module-as-singleton controlling the panels. Works with ui.py."""

import typing as t

import rich

import env
import ui

panel_stack: t.List[ui.Panel] = []

screen0: env.Screen = [[""] * env.term_width for _ in range(env.term_height)]
screen1: env.Screen = [[""] * env.term_width for _ in range(env.term_height)]
screen_to_render: env.Screen = screen0


def render() -> None:
    """Composite live panels to a screen."""
    global screen_to_render

    num_of_cells_to_render: int = env.term_height * env.term_width
    rendered: t.List[t.List[bool]] = [[False] * env.term_width for _ in range(env.term_height)]
    for p in reversed(panel_stack):
        num_of_cells_to_render -= p.render(rendered, screen_to_render)
        if num_of_cells_to_render <= 0:
            break
    print_screen(screen_to_render)

    screen_to_render = screen0 if screen_to_render == screen1 else screen1


def print_screen(screen_to_render: env.Screen) -> None:
    """Print a screen on terminal."""
    old_screen = screen0 if screen_to_render == screen1 else screen1
    for i in range(env.term_height):
        for j in range(env.term_width):
            with env.term.location(j, i):  # NB blessed uses x, y
                if screen_to_render[i][j] != old_screen[i][j]:
                    rich.print(screen_to_render[i][j])
