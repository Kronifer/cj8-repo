"""This is a module-as-singleton controlling the panels. Works with ui.py."""

import typing as t

import rich

import env
import ui

panel_stack: t.List[ui.Panel] = []


def render() -> None:
    """Composite live panels to a screen."""
    screen_to_render: env.Screen = [[""] * env.term_width for _ in range(env.term_height)]
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
