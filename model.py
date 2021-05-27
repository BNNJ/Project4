#!/usr/bin/env python3

from tinydb import TinyDB, where


###############################################################################
# PLAYER
###############################################################################

class Player:
    def __init__(self, first_name, last_name, gender,
                 birth_date, rank, _id=None, **kwargs):
        self.first_name = first_name.title()
        self.last_name = last_name.title()
        self.birth_date = birth_date
        self.rank = rank
        self.gender = gender.lower()
        self._id = _id or len(TinyDB(TOURNAMENTS_DB).all())
        self.score = 0

    def serialize(self):
        return self.__dict__

    def save(self):
        db = TinyDB(PLAYERS_DB)
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
        return (f"{self._id}: {self.first_name + ' ' + self.last_name:<24}"
                f" rank:{self.rank}\tscore:{self.score}")

    def __repr__(self):
        return f"{self.first_name} {self.last_name}"


def new_player(first_name, last_name, gender, birth_date, rank):
    return Player(first_name, last_name, gender, birth_date, rank)


def get_player(_id):
    player = TinyDB(PLAYERS_DB).get(doc_id=_id)
    if player is not None:
        return Player(**player)


def list_players():
    players = TinyDB(PLAYERS_DB).all()
    if len(players) > 0:
        return {
            f"{str(p.doc_id):<3}: {p['first_name']} {p['last_name']}": (
                f"gender:     {p['gender']}\n"
                f"birth_date: {p['birth_date']}\n"
                f"rank:       {p['rank']}"
            ) for p in players
        }


def get_players(ids):
    return [get_player(i) for i in ids]


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
                 description="", rounds_max=4, rounds=[], round_started=False,
                 current_round=1, _id=None, **kwargs):
        self.name = name
        self.location = location
        self.date = date
        self.players = get_players(players)
        self.players_count = len(players)
        self.time_format = time_format
        self.description = description
        self.rounds_max = rounds_max
        self.rounds = rounds
        self.round_started = round_started
        self.current_round = current_round
        self._id = _id or len(TinyDB(TOURNAMENTS_DB).all())
        self.previously_played = {}

    def serialize(self):
        t = self.__dict__
        t['players'] = [p._id for p in self.players]
        return t

    def save(self):
        db = TinyDB(TOURNAMENTS_DB)
        tourney = db.get(where('name') == self.name)
        if tourney is None:
            db.insert(self.serialize())
        else:
            db.update(self.serialize(), doc_ids=[tourney.doc_id])

    def update_scores(self, players):
        self.score = {p._id: p.score for p in players}

    def __str__(self):
        return f"{self.name} ({self._id}): {self.location} on {self.date}"

    def __repr__(self):
        return f"{self.name} ({self._id}): {self.location} on {self.date}"


def load_tournament(_id):
    tourney = TinyDB(TOURNAMENTS_DB).get(doc_id=_id)
    if tourney is not None:
        return Tournament(**tourney)


def list_tournaments():
    tournaments = TinyDB(TOURNAMENTS_DB).all()
    if len(tournaments) > 0:
        return {
            t['name']: (
                f"location:    {t['location']}\n"
                f"date:        {t['date']}\n"
                f"players:     {t['players']}\n"
                f"time format: {t['time_format']}\n"
                f"description: {t['description']}\n"
            ) for t in tournaments
        }

###############################################################################


def clear_table(table):
    TinyDB(table).truncate()


def start(players_db, tournaments_db):
    global PLAYERS_DB
    PLAYERS_DB = players_db
    global TOURNAMENTS_DB
    TOURNAMENTS_DB = tournaments_db
