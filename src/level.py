import pickle
from pathlib import Path


def load_levels() -> list:
    """Loads all levels from the levels directory."""
    p = Path("./levels")
    levels = list(p.glob("*.level"))
    for element in levels:
        index = levels.index(element)
        with open(element, 'rb') as f:
            levels[index] = pickle.load(f)
    try:
        with open('saves/main.save', 'rb') as f:
            otherlevels = pickle.load(f)
        return otherlevels
    except EOFError:
        return levels
    except FileNotFoundError:
        return levels
