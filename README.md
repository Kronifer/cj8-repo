# Python Discord Code Jam #8 - Transcendent Tarsiers

## Who are we?
 - [Kronifer](https://github.com/Kronifer)
 - [12944qwerty](https://github.com/12944qwerty)
 - [Jetsie](https://github.com/Jetsie)
 - [grivera64](https://github.com/grivera64)
 - [ufshaikh](https://github.com/ufshaikh)

## Our Project

We created a game called _Packed_, where each level takes place in a box. You enter another dimension
each time you reach the end of a level.

# Contributing

We use Poetry to manage our dependancies, among other things. To install it, run `pip install poetry`.
In your cloned repository, after you've installed poetry, run the following commands:
```sh
poetry install
poetry run pre-commit install
```
This will install our dependancies, and a tool called pre-commit. It will block you from committing if your
lint fails. It is required that you install it. If you want to check your lint at any time, simply run `poetry run task lint` and poetry will lint for you.
If your lint fails in any pull request or commit, that pull request will not be merged, and if the commit is to main, it will be reverted, so be careful.

## Level Creator

The Level Creator file in the tools folder is part of the full game, but NOT the TUI. It is used to
allow users to create custom levels.

# Installing

To install _Packed_, clone the repository and run `poetry install`. The dependancies are now
installed. To run the game, simply run `poetry run task start` in the project's root directory with
a maximized or fullscreen terminal that supports color.
