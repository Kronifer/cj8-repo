"""Player class."""

import env

SOLIDS: list = ["GRASS", "FLOOR", "SPIKE_UP", "SPIKE_DOWN", "STONE", "LAVA"]


class Player:
    """This is the player's ingame object.

    Only one should ever exist at a time.

    TODO: either this should eventually inherit from an entity class or be made
    into a module as singleton.
    """

    def __init__(self, world: list, backupworld: list):
        self.world = world
        self.checkworld = backupworld
        self.jumping = False

    def move_left(self) -> None:
        """Move the player one cell left."""
        for element in self.world:
            worldindex = self.world.index(element)
            try:
                index = element.index("PLAYER")
                break
            except ValueError:
                pass
        if self.world[worldindex][index - 1] in SOLIDS:
            pass
        elif index - 1 < 0:
            pass
        else:
            self.world[worldindex][index] = self.checkworld[worldindex][index] if \
                self.checkworld[worldindex][index] != "PLAYER" else "AIR"
            self.world[worldindex][index - 1] = "PLAYER"

    def move_right(self) -> None:
        """Move the player one cell right."""
        for element in self.world:
            worldindex = self.world.index(element)
            try:
                index = element.index("PLAYER")
                break
            except ValueError:
                pass
        if index + 1 == len(self.world[worldindex]):
            pass
        elif self.world[worldindex][index + 1] in SOLIDS:
            pass
        elif (index + 1) >= len(self.world[worldindex]):
            pass
        else:
            self.world[worldindex][index] = self.checkworld[worldindex][index] if \
                self.checkworld[worldindex][index] != "PLAYER" else "AIR"
            self.world[worldindex][index + 1] = "PLAYER"

    def jump(self) -> None:
        """Make the player begin a jump if in position to jump."""
        if self.jumping:
            self.jumping = False
            self.move_down()
        for element in self.world:
            worldindex = self.world.index(element)
            try:
                index = element.index("PLAYER")
                break
            except ValueError:
                pass
        if self.world[worldindex + 1][index] in SOLIDS:
            if self.world[worldindex - 1][index] == "SPIKE_DOWN":
                env.hits -= 1
            if self.world[worldindex - 1][index] in SOLIDS:
                pass
            elif worldindex == 0:
                pass
            else:
                self.world[worldindex][index] = self.checkworld[worldindex][index] if \
                    self.checkworld[worldindex][index] != "PLAYER" else "AIR"
                self.world[worldindex - 1][index] = "PLAYER"
                self.jumping = True
        else:
            self.move_down()

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
            self.world[worldindex][index] = self.checkworld[worldindex][index]
            self.world[worldindex + 1][index] = "PLAYER"
