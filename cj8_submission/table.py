from typing import Any, List, Optional

CHARACTERS = {"SIDE_CHARACTER": "│", "TOP_AND_BOTTOM_CHARACTER": "─", "TOP_LEFT_CORNER": "┌",
              "TOP_SPLIT": "┬", "TOP_RIGHT_CORNER": "┐", "SIDE_LEFT_SPLIT": "├", "FOUR_WAY_SPLIT": "┼",
              "SIDE_RIGHT_SPLIT": "┤", "BOTTOM_LEFT_CORNER": "└", "BOTTOM_SPLIT": "┴",
              "BOTTOM_RIGHT_CORNER": "┘"
              }


def make_table(rows: List[List[Any]], labels: Optional[List[Any]] = None, centered: bool = False,
               colored: bool = False, characters: dict = CHARACTERS
               ) -> str:
    """Creates a table from the given parameters."""
    # Creates a list of each column in the table
    columns = []
    if labels:
        for i in range(len(labels)):
            column = []
            for element in rows:
                column.append(str(element[i]))
            column.append(str(labels[i]))
            columns.append(column)
    else:
        for i in range(len(rows[0])):
            column = []
            for element in rows:
                column.append(str(element[i]))
            columns.append(column)
    # Creates a list of the longest element in each column
    longests = []
    for element in columns:
        longest = len(max(element, key=len))
        longests.append(longest)
    for element in columns:
        longest = longests[columns.index(element)]
        for elem in element:
            index = element.index(elem)
            if len(elem) < longest:
                if centered:
                    for i in range(longest - len(elem)):
                        if i == 0 or i % 2 == 0:
                            elem += " "
                        else:
                            elem = f" {elem}"
                else:
                    for i in range(longest - len(elem)):
                        elem += " "
            elem = f"{characters['SIDE_CHARACTER']} {elem} "
            element[index] = elem
    # Adds the side character to the end of all elements in the last column
    for element in columns[-1]:
        index = columns[-1].index(element)
        element = f"{element} {characters['SIDE_CHARACTER']}"
        columns[-1][index] = element
    # Compiles the columns into rows
    newrows = []
    for i in range(len(columns[0]) - 1 if labels else len(columns[0])):
        row = []
        for element in columns:
            row.append(element[i])
        newrows.append(''.join(row))
    if labels:
        # Creates the label string if labels exist
        newlabels = ''.join([element[-1] for element in columns])
    splits = []
    for i in range(len(columns) - 1):
        splits.append(
            newrows[0].index(characters['SIDE_CHARACTER'], 1) if i == 0
            else newrows[0].index(characters['SIDE_CHARACTER'], splits[i - 1] + 1)
        )
    topbar = characters["TOP_LEFT_CORNER"] if not labels else characters["SIDE_LEFT_SPLIT"]
    for i in range(len(newrows[0]) - 2):
        if splits.count(i + 1) >= 1:
            topbar += characters["TOP_SPLIT"] if not labels else characters["FOUR_WAY_SPLIT"]
            continue
        topbar += characters["TOP_AND_BOTTOM_CHARACTER"]
    topbar += characters["TOP_RIGHT_CORNER"] if not labels else characters["SIDE_RIGHT_SPLIT"]
    newrows.insert(0, topbar)
    bottombar = characters["BOTTOM_LEFT_CORNER"]
    for i in range(len(newrows[0]) - 2):
        if splits.count(i + 1) >= 1:
            bottombar += characters["BOTTOM_SPLIT"]
            continue
        bottombar += characters["TOP_AND_BOTTOM_CHARACTER"]
    bottombar += characters["BOTTOM_RIGHT_CORNER"]
    newrows.append(bottombar)
    if labels:
        newrows.insert(0, newlabels)
        topbar = characters["TOP_LEFT_CORNER"]
        for i in range(len(newrows[0]) - 2):
            if splits.count(i + 1) >= 1:
                topbar += characters["TOP_SPLIT"]
                continue
            topbar += characters["TOP_AND_BOTTOM_CHARACTER"]
        topbar += characters["TOP_RIGHT_CORNER"]
        newrows.insert(0, topbar)
    return '\n'.join(newrows)
