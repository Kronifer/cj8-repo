"""Custom Exceptions"""


class TooManySelected(Exception):
    """Raised when too many TextWidgetEntries are "selected" entries."""

    def __init__(self, message: str = "Too many entries were selected."):
        super().__init__(message)
