# Used to allow access to src file
import sys

sys.path.append("../")

from keypress import Trigger  # noqa: E402,I001

    # noqa: I005,I003,E116

trigger = Trigger(0)

value: str

with trigger.term.cbreak():
    while not (value := trigger.get_input()):

        continue

print("Input found!", value)
