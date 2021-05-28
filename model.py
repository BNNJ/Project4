#!/usr/bin/env python3

import operator
from tinydb import TinyDB, where
from datetime import datetime

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
        self._id = _id or len(TinyDB(TOURNAMENTS_DB)) + 1
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
    with open('log2.txt', 'a') as f:
        f.write(f"{ids}\n")
    return [get_player(i) for i in ids]


###############################################################################
# MATCH
###############################################################################

class Match:

    SCORE_MAP = {
        'white': [1, 0],
        'black': [0, 1],
        'draw': [0.5, 0.5]
    }

    def __init__(self, white, black, result=None):
        self.white = get_player(white[0])
        self.black = get_player(black[0])
        self.white_score = white[1]
        self.black_score = black[1]

    def set_score(self, result):
        self.white_score = self.SCORE_MAP[result][0]
        self.black_score = self.SCORE_MAP[result][1]
        self.white.score += self.white_score
        self.black.score += self.black_score

    def serialize(self):
        return (
            [self.white._id, self.white_score],
            [self.black._id, self.black_score],
        )


###############################################################################
# ROUND
###############################################################################


class Round:
    def __init__(self, name, matches=[], start_time=None, end_time=None):
        self.name = name
        self.matches = [Match(m[0], m[1]) for m in matches]
        self.start_time = start_time
        self.end_time = end_time

    def start(self):
        self.start_time = datetime.now().strftime('%Y/%m/%d %H:%M:%S')

    def end(self, results):
        self.end_time = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        [m.set_score(results[i]) for i, m in enumerate(self.matches)]

    def serialize(self):
        return {
            'name': self.name,
            'matches': [m.serialize() for m in self.matches],
            'start_time': self.start_time,
            'end_time': self.end_time
        }

###############################################################################
# TOURNAMENT
###############################################################################


class Tournament:
    def __init__(self, name, location, date, players, time_format,
                 description="", max_round=4, rounds=[], round_started=False,
                 round_nb=0, _id=None, previously_played=None, score=None):
        self.name = name
        self.location = location
        self.date = date
        self.players = get_players(players)
        self.players_count = len(players)
        self.time_format = time_format
        self.description = description
        self.rounds = [Round(**r) for r in rounds]
        self.max_round = max_round
        self.round_nb = round_nb
        self.round_started = round_started
        self.current_round = None if round_nb == 0 else self.rounds[round_nb-1]
        self._id = _id or len(TinyDB(TOURNAMENTS_DB)) + 1
        self.previously_played = previously_played or {i: [] for i in players}
        self.score = score or {i: 0 for i in players}

    def end(self):
        pass

    def start_round(self):
        if self.round_nb < self.max_round:
            self.round_started = True
            matchups = self.swiss_sort()
            matches = [([m[0], 0], [m[1], 0]) for m in matchups]
            r = Round(f"round{self.round_nb}", matches)
            self.rounds.append(r)
            self.current_round = self.rounds[self.round_nb]
            self.current_round.start()
            self.round_nb += 1
        else:
            self.end()

    def end_round(self, results):
        self.round_started = False
        if self.round_nb == self.max_round:
            self.end()
        else:
            self.current_round.end(results)
            for p in self.players:
                self.score[p._id] = p.score

    def serialize(self):
        # t = dict(self.__dict__)
        # t['players'] = [p._id for p in self.players]
        # t['rounds'] = [r.serialize() for r in self.rounds]
        # del t['current_round']
        # del t['players_count']
        # return t
        return {
            'name': self.name,
            'location': self.location,
            'date': self.date,
            'players': [p._id for p in self.players],
            'time_format': self.time_format,
            'description': self.description,
            'rounds': [r.serialize() for r in self.rounds],
            'max_round': self.max_round,
            'round_nb': self.round_nb,
            'round_started': self.round_started,
            'previously_played': self.previously_played,
            '_id': self._id,
            'score': self.score
        }

    def save(self):
        db = TinyDB(TOURNAMENTS_DB)
        db.upsert(self.serialize(), where('_id') == self._id)
        # tournament = db.get(where('name') == self.name)
        # if tournament is None:
        #     db.insert(self.serialize())
        # else:
        #     db.update(self.serialize(), doc_ids=[tournament.doc_id])

    def swiss_sort(self):
        players = sorted(self.players, key=operator.attrgetter('rank'))
        if self.round_nb > 0:
            players = sorted(players, key=operator.attrgetter('score'))
            players = [p._id for p in players]
            if players[1] in self.previously_played[players[0]]:
                players[0], players[1] = players[1], players[0]
            matchups = [
                (players[0], players[1]),
                (players[2], players[3]),
                (players[4], players[5]),
                (players[6], players[7])
            ]
        else:
            players = [p._id for p in players]
            pivot = len(players) // 2
            matchups = list(zip(players[:pivot], players[pivot:]))
        for w, b in matchups:
            self.previously_played[w].append(b)
            self.previously_played[b].append(w)
        return matchups

    def __str__(self):
        return f"{self.name} ({self._id}): {self.location} on {self.date}"

    def __repr__(self):
        return f"{self.name} ({self._id}): {self.location} on {self.date}"


def load_tournament(_id):
    tournament = TinyDB(TOURNAMENTS_DB).get(doc_id=_id)
    if tournament is not None:
        return Tournament(**tournament)


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
