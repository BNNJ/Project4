#!/usr/bin/env python3

import operator
from model import *
from tinydb import *


def swiss_sort(players, prev, score, r):
    players = sorted(players, key=operator.attrgetter('rank'))
    if r > 0:
        players = sorted(players, key=operator.attrgetter('score'))
        if players[1].id in prev[players[0].id]:
            players[0], players[1] = players[1], players[0]
    players = [p.id for p in players]
    pivot = len(players) // 2
    matchups = list(zip(players[:pivot], players[pivot:]))
    for b, w in matchups:
        prev[b].append(w)
        prev[w].append(b)
    return matchups


def main():
    players = get_players(range(1, 9))

    [print(p) for p in players]
    print("\n##################\n")

    previous_matchups = {p.id: [] for p in players}
    score = {p.id: 0 for p in players}
    for round_count in range(5):
        matchups = swiss_sort(players, previous_matchups, score, round_count)
    #   print(f"round {round_count + 1}:")
    #   [print(b, w) for (b, w) in matchups]
    #   for p in players:
    #       p.score += randrange(30)
    # print(previous_matchups)

    # [print(p) for p in get_players()]


if __name__ == "__main__":
    main()
