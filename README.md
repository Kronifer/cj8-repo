# Python Discord Code Jam #8 - Transcendent Tarsiers

## Who are we?
 - [Kronifer](https://github.com/Kronifer)
 - [12944qwerty](https://github.com/12944qwerty)
 - [Jetsie](https://github.com/Jetsie)
 - [grivera64](https://github.com/grivera64)
 - [ufshaikh](https://github.com/ufshaikh)

## Our Project
We decided on making a game. This game is platformer-styled. Each level is inside a box.

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
