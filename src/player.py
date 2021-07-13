"""Player class."""


class Player:
    """This is the player's ingame object.

    Only one should ever exist at a time.

    TODO: either this should eventually inherit from an entity class or be made
    into a module as singleton.
    """

    def __init__(self):
        pass

    def move_left(self) -> None:
        """Move the player one cell left."""
        pass

    def move_right(self) -> None:
        """Move the player one cell right."""
        pass

    def jump(self) -> None:
        """Make the player begin a jump if in position to jump."""
        pass
