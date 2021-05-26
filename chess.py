#!/usr/bin/env python3

import os
import operator
import controller

# from random import randrange

def swiss_sort(players, prev, score, r):
    players = sorted(players, key=operator.attrgetter('rank'))
    if r > 0:
        players = sorted(players, key=operator.attrgetter('score'))
        if players[1].id in prev[players[0].id]:
            players[0], players[1] = players[1], players[0]
    # players = [p.id for p in players]
    pivot = len(players) // 2
    matchups = list(zip(players[:pivot], players[pivot:]))
    for b, w in matchups:
        prev[b.id].append(w.id)
        prev[w.id].append(b.id)
    return [Match(b, w) for b, w in matchups]

def test():
    players = [
        new_player("Jimmy", "Page", "M", 0, 1),
        new_player("John Paul", "Jones", "M", 0, 2),
        new_player("Robert", "Plant", "M", 0, 3),
        new_player("John", "Bonham", "M", 0, 4),
        new_player("Ian", "Paice", "M", 0, 5),
        new_player("Ritchie", "Blackmore", "M", 0, 6),
        new_player("Ian", "Gillan", "M", 0, 7),
        new_player("Roger", "Glover", "M", 0, 8)
    ]
    [p.save() for p in players]

    tournament = (
        "bla",
        "Djakarta",
        0,
        [p.id for p in players],
        "Blitz"
    )
    tournament.save()

possible_results = ['black', 'white', 'draw']
SCORE_MAP = {
    'black': [1, 0],
    'white': [0, 1],
    'draw': [0.5, 0.5]
}


def size_check():
    term_size = os.get_terminal_size()
    rows = term_size.lines
    cols = term_size.columns
    return (rows >= 30 and cols >= 80)

def main():
    # model.clear_table('tournament.json')
    if size_check:
        controller.start()
    else:
        print("That terminal is too small for such a big program !")

if __name__ == "__main__":
    main()
