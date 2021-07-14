"""Player class."""

SOLIDS: list = ["GRASS", "FLOOR", "SPIKE_UP", "SPIKE_DOWN", "STONE"]


class Player:
    """This is the player's ingame object.

    Only one should ever exist at a time.

    TODO: either this should eventually inherit from an entity class or be made
    into a module as singleton.
    """

    def __init__(self, world: list):
        self.world = world

    def move_left(self) -> None:
        """Move the player one cell left."""
        for element in self.world:
            worldindex = self.world.index(element)
            try:
                index = element.index("PLAYER")
            except ValueError:
                pass
            if "index" in locals():
                break
        if self.world[worldindex][index - 1] in SOLIDS:
            pass
        else:
            self.world[worldindex][index] = "AIR"
            self.world[worldindex][index - 1] = "PLAYER"

    def move_right(self) -> None:
        """Move the player one cell right."""
        for element in self.world:
            worldindex = self.world.index(element)
            try:
                index = element.index("PLAYER")
            except ValueError:
                pass
            if "index" in locals():
                break
        if self.world[worldindex][index - 1] in SOLIDS:
            pass
        else:
            self.world[worldindex][index] = "AIR"
            self.world[worldindex][index - 1] = "PLAYER"

    def jump(self) -> None:
        """Make the player begin a jump if in position to jump."""
        for element in self.world:
            worldindex = self.world.index(element)
            try:
                index = element.index("PLAYER")
            except ValueError:
                pass
            if "index" in locals():
                break
        if self.world[worldindex + 1][index] not in SOLIDS or self.world[worldindex - 1][index] in SOLIDS:
            pass
        else:
            self.world[worldindex][index] = "AIR"
            self.world[worldindex - 1][index] = "PLAYER"

    def move_down(self) -> None:
        """Moves the player down a cell if no solid cell is under the player."""
        for element in self.world:
            worldindex = self.world.index(element)
            try:
                index = element.index("PLAYER")
            except ValueError:
                pass
            if "index" in locals():
                break
        if self.world[worldindex + 1][index] in SOLIDS:
            pass
        else:
            self.world[worldindex][index] = "AIR"
            self.world[worldindex + 1][index] = "PLAYER"
