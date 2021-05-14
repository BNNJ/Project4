#!/usr/bin/env python3

from tinydb import TinyDB, Query, where
from enum import Enum

class Gender(Enum):
	UNKNOWN = 0
	MALE = 1
	FEMALE = 2

class TimeFormat(Enum):
	BLITZ = 0
	BULLET = 1
	FAST = 2

#################################### PLAYER ####################################

class Player:
	def __init__(self, first_name, last_name, gender, birth_date, rank, _id=0):
		self.first_name = first_name.title()
		self.last_name = last_name.title()
		self.birth_date = birth_date
		self.rank = rank
		if gender.lower() in ["m", "male", "man", "boy", "guy", "dude"]:
			self.gender = Gender.MALE
		elif gender.lower() in ["f", "female", "woman", "girl"]:
			self.gender = Gender.FEMALE
		else:
			self.gender = Gender.UNKNOWN
		self.id = _id

	def serialize(self):
		d = self.__dict__
		d['gender'] = "M" if self.gender == Gender.MALE else "F"
		return d

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

	def update(self, value):
		TinyDB('players.json').upsert(
			value,
			Query().first_name == self.first_name
		)

	def change_rank(self, rank):
		self.rank = rank

	def __str__(self):
		return (f"{self.first_name} {self.last_name} ({self.id}): rank:{self.rank}")
	def __repr__(self):
		return (f"{self.first_name} {self.last_name} ({self.id}): rank:{self.rank}")

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
			_id=player.doc_id
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
			_id=player.doc_id
		)
	else:
		return None

def get_players(ids):
	return [get_player(i) for i in ids]


#################################### MATCH #####################################

class Round:
	pass

class Match:
	pass


################################## TOURNAMENT ##################################

class Tournament:
	def __init__(self, name, location, date, players, time_format,
				description="", rounds_max=4, _id=0):
		self.name = name
		self.location = location
		self.date = date
		self.players = players
		self.players_count = len(players)
		self.time_format = time_format
		self.description = description
		self.rounds_max = rounds_max
		self.matches = []
		self.rounds = []
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



################################################################################

def clear_table(table):
	TinyDB(table).truncate()
