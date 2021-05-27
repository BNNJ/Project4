#!/usr/bin/env python3

import os
import argparse
from controller import start


def parse_args():
    argp = argparse.ArgumentParser(description="Chess tournament organizer")

    argp.add_argument(
        "-p", "--players",
        default="players.json",
        help="The players database"
    )

    argp.add_argument(
        "-t", "--tournaments",
        default="tournaments.json",
        help="The tournaments database"
    )

    return argp.parse_args()


def size_check():
    term_size = os.get_terminal_size()
    rows = term_size.lines
    cols = term_size.columns
    return (rows >= 30 and cols >= 80)


def main():
    if size_check:
        args = parse_args()
        start(args.players, args.tournaments)
    else:
        print("That terminal is too small for such a big program !")


if __name__ == "__main__":
    main()
