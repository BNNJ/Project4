#!/usr/bin/env python3

import operator
from random import randrange
from enum import Enum

class Tournament:
	def __init__(self, name, location, date, players, time_format,
				description="", rounds_max=4):
		self.name = name
		self.location = location
		self.date = date
		self.players = players
		self.players_count = len(players)
		self.time_format = time_format
		self.description = description
		self.rounds_max = rounds_max
		self.matchups = [[False] * self.players_count] * self.players_count

class Gender(Enum):
	UNKNOWN = 0
	MALE = 1
	FEMALE = 2

class TimeFormat(Enum):
	BLITZ = 0
	BULLET = 1
	FAST = 2

class Player:
	__id = 0
	
	def __init__(self, first_name, last_name, gender, birth_date, rank):
		self.first_name = first_name
		self.last_name = last_name
		self.birth_date = birth_date
		self.rank = rank
		if gender.lower() in ["m", "male", "man", "boy", "guy", "dude"]:
			self.gender = Gender.MALE
		elif gender.lower() in ["f", "female", "woman", "girl"]:
			self.gender = Gender.FEMALE
		else:
			self.gender = Gender.UNKNOWN
		self.score = 0
		self.id = Player.__id
		Player.__id += 1

	def __str__(self):
		return (f"{self.first_name} {self.last_name}: {self.rank}")
	def __repr__(self):
		return (f"{self.first_name} {self.last_name}: {self.rank}")

def swiss_sort(players, prev, r):
	players = sorted(players, key=operator.attrgetter('rank'))
	if r == 0:
		players = [p.id for p in players]
		pivot = len(players) // 2
		matchups = list(zip(players[:pivot], players[pivot:]))
	else:
		players = [p.id for p in sorted(players, key=operator.attrgetter('score'))]
		matchups = []
		while players:
			b = players.pop()
			# w = players.pop() if players[0] not in prev[b] else players.pop(1)
			if players[0] not in prev[b] or len(players) == 1:
				w = players.pop()
			else:
				w = players.pop(1)
			matchups.append((b, w))
	for b, w in matchups:
		prev[b].append(w)
		prev[w].append(b)
	return matchups

def main():

	players = [
		Player("John Paul", "Jones", "M", "0", 14),
		Player("John", "Bonham", "M", "0",4),
		Player("Jimmy", "Page", "M", "0", 25),
		Player("Robert", "Plant", "M", "0", 8),
		Player("Ritchie", "Blackmore", "M", "0", 6),
		Player("Ian", "Paice", "M", "0", 2),
		Player("Ian", "Gillan", "M", "0", 21),
		Player("Roger", "Glover", "M", "0", 19),
	]
	tournament = Tournament(
		name = "whatev",
		location = "Djakarta",
		date = "123",
		players = players,
		time_format = TimeFormat.BLITZ,
	)

	previous_matchups = {p.id: [] for p in players}

	for round_count in range(0, tournament.rounds_max):
		matchups = swiss_sort(players, previous_matchups, round_count)
		print(f"round {round_count}:")
		[print(b, w) for (b, w) in matchups]
		for p in players:
			p.score += randrange(30)
		# print(previous_matchups)

if __name__ == "__main__":
	main()
