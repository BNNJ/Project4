#!/usr/bin/env python3

import os
import argparse
from controller import start


# import operator
# def swiss_sort(players, prev, score, r):
#     players = sorted(players, key=operator.attrgetter('rank'))
#     if r > 0:
#         players = sorted(players, key=operator.attrgetter('score'))
#         if players[1].id in prev[players[0].id]:
#             players[0], players[1] = players[1], players[0]
#     # players = [p.id for p in players]
#     pivot = len(players) // 2
#     matchups = list(zip(players[:pivot], players[pivot:]))
#     for b, w in matchups:
#         prev[b.id].append(w.id)
#         prev[w.id].append(b.id)
#     return [Match(b, w) for b, w in matchups]

possible_results = ['black', 'white', 'draw']
SCORE_MAP = {
    'black': [1, 0],
    'white': [0, 1],
    'draw': [0.5, 0.5]
}


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
