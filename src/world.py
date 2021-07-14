# Name: world.py
# Purpose: Represents the data form of the world
# Author: @grivera64
# Date: July 2021

SOLIDS: list = ["GRASS", "FLOOR", "SPIKE_UP", "SPIKE_DOWN", "STONE"]


def apply_gravity(world: list[list[str]]) -> None:
    """Applies gravity to non-solid entities in the world

    :param world: The world in a 2D array
    """
    rows = len(world)
    cols = len(world[0])

    for row in range(rows - 1, 0, -1):

        for col in range(cols):

            # Drop the not-solid text above air
            if "AIR" in world[row][col]:

                if world[row - 1][col] not in SOLIDS:

                    tmp = world[row][col]
                    world[row][col] = world[row - 1][col]
                    world[row - 1][col] = tmp

    pass
