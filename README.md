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

# Installing

To install _Packed_, clone the repository or download version 1.0.0 from the Releases tab and run `poetry install`. The dependancies are now
installed. To run the game, simply run `poetry run task start` in the project's root directory with
a maximized or fullscreen terminal that supports color.

## How To Play
When you start the game, you will be brought to a menu screen with 4 options (unfortunately, the second option does not work due to time constraints). You can use the highlighter to navigate and choose an option.

Each level is pretty simple and displays many mechanics we've developed in the game. There are two solid blocks (rock and grass), two kill blocks (spikes and lava) and the other components (player, end, and water). Water does not have any affect on gameplay yet. It is used for decoration and pits.

Fortunately (and unfortunately), the physics is a bit buggy. One of the most profound ~~bugs~~ features we made was to dash in the middle of the air. This takes some practice to master, but if you spam in a direction, you will be able to stay on one level for quite a while. We leave it up to you to find the rest.

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

# Notes

 - The Level Creator file in the tools folder was used for development purposes only. It was used to help us visualize the levels we wanted to make. It should not be considered a part of the TUI game. However, it is included in the repo for modders.
 - There are still multiple bugs that we were unable to fix before the deadline. They are listed below:
   + Saving just before taking damage and reloading the game can give you the game over screen on the main menu, forcing you to empty your save files contents.
   + If you do the above thing but instead load your save in-game, your game will also crash.
   + Not particularly a bug, but our hit detection is quite finnicky and may make the game a challenge to beat.
 - For the full experience, please play in a full-sized terminal with support for colors.
