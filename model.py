#!/usr/bin/env python3

from tinydb import TinyDB, where
from enum import Enum


# class Gender(Enum):
#     UNKNOWN = 0
#     MALE = 1
#     FEMALE = 2


# class TimeFormat(Enum):
#     BLITZ = 0
#     BULLET = 1
#     FAST = 2


###############################################################################
# PLAYER
###############################################################################

class Player:
    def __init__(self, first_name, last_name, gender,
                 birth_date, rank, _id=None):
        self.first_name = first_name.title()
        self.last_name = last_name.title()
        self.birth_date = birth_date
        self.rank = rank
        self.gender = gender.lower()
        self.id = _id
        self.score = 0

    def serialize(self):
        return self.__dict__

    def save(self):
        db = TinyDB('players.json')
        player = db.get(
            (where('first_name') == self.first_name)
            & (where('last_name') == self.last_name)
        )
        if player is None:
            db.insert(self.serialize())
        else:
            db.update(self.serialize(), doc_ids=[player.doc_id])

    def change_rank(self, rank):
        self.rank = rank

    def __str__(self):
        return (f"{self.first_name} {self.last_name} ({self.id}):"
                f" rank:{self.rank}\tscore:{self.score}")

    def __repr__(self):
        return (f"{self.first_name} {self.last_name} ({self.id}):"
                f" rank:{self.rank}\tscore:{self.score}")


# Player functions

def new_player(first_name, last_name, gender, birth_date, rank):
    return Player(first_name, last_name, gender, birth_date, rank)


def get_player_by_name(first_name, last_name):
    player = TinyDB('players.json').get(
        (where('first_name') == first_name.title())
        & (where('last_name') == last_name.title())
    )
    if player is not None:
        return Player(
            player['first_name'],
            player['last_name'],
            player['gender'],
            player['birth_date'],
            player['rank'],
            player.doc_id
        )
    else:
        return None


def get_players_by_name(names):
    return [get_player_by_name(fn, ln) for (fn, ln) in names]


def get_player(_id):
    player = TinyDB('players.json').get(doc_id=_id)
    if player is not None:
        return Player(
            player['first_name'],
            player['last_name'],
            player['gender'],
            player['birth_date'],
            player['rank'],
            player.doc_id
        )
    else:
        return None


def get_players(ids):
    return [get_player(i) for i in ids]


def show_players():
    [print(p) for p in TinyDB('players.json').all()]


###############################################################################
# MATCH
###############################################################################

class Match:
    def __init__(self, black, white, result=None):
        self.black = black
        self.white = white
        self.result = result


###############################################################################
# ROUND
###############################################################################

class Round:
    def __init__(self, matches=[]):
        self.matches = matches


###############################################################################
# TOURNAMENT
###############################################################################

class Tournament:
    def __init__(self, name, location, date, players, time_format,
                 description="", rounds_max=4, matches=[],
                 rounds=[], score={}, _id=None):
        self.name = name
        self.location = location
        self.date = date
        self.players = players
        self.players_count = len(players)
        self.time_format = time_format
        self.description = description
        self.rounds_max = rounds_max
        self.matches = matches
        self.rounds = rounds
        self.score = score
        self.id = _id

    def serialize(self):
        return self.__dict__

    def save(self):
        db = TinyDB('tournaments.json')
        tourney = db.get(where('name') == self.name)
        if tourney is None:
            db.insert(self.serialize())
        else:
            db.update(self.serialize(), doc_ids=[tourney.doc_id])

    def update_scores(self, players):
        self.score = {p.id: p.score for p in players}

    def get_players(self):
        players = get_players(self.players)
        for p in players:
            p.score = self.score[p.id]
        return players

    def __str__(self):
        return f"{self.name} ({self.id}): {self.location} on {self.date}"

    def __repr__(self):
        return f"{self.name} ({self.id}): {self.location} on {self.date}"


def new_tournament(name, location, date, players, time_format):
    return Tournament(name, location, date, players, time_format)


def load_tournament(name):
    tourney = TinyDB('tournaments.json').get(where('name') == name)
    return Tournament(
        tourney['name'],
        tourney['location'],
        tourney['date'],
        tourney['players'],
        tourney['time_format'],
        tourney['description'],
        tourney['rounds_max'],
        tourney['matches'],
        tourney['rounds'],
        tourney['score'],
        _id=tourney.doc_id
    )


###############################################################################

def clear_table(table):
    TinyDB(table).truncate()
