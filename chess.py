#!/usr/bin/env python3

import operator
from model import *
from tinydb import *

def swiss_sort(players, prev, r):
	players = sorted(players, key=operator.attrgetter('rank'))
	if r > 0:
		players = sorted(players, key=operator.attrgetter('score'))
		if players[1].id in prev[players[0]]:
			players[0], players[1] = players[1], players[0]
	players = [p.id for p in players]
	pivot = len(players) // 2
	matchups = list(zip(players[:pivot], players[pivot:]))
	for b, w in matchups:
		prev[b].append(w)
		prev[w].append(b)
	return matchups

def main():
	# clear_table('players.json')
	# players = [
	# 	new_player("John Paul", "Jones", "M", "0", 14),
	# 	new_player("John", "Bonham", "M", "0",4),
	# 	new_player("Jimmy", "Page", "M", "0", 25),
	# 	new_player("Robert", "Plant", "M", "0", 8),
	# 	new_player("Ritchie", "Blackmore", "M", "0", 6),
	# 	new_player("Ian", "Paice", "M", "0", 2),
	# 	new_player("Ian", "Gillan", "M", "0", 21),
	# 	new_player("Roger", "Glover", "M", "0", 19),
	# ]
	# [p.save() for p in players]
	# [print(p.id) for p in players]
	

	print(get_player_by_name("Ian", "Paice"))


	# tournament = Tournament(
	# 	name = "whatev",
	# 	location = "Djakarta",
	# 	date = "123",
	# 	players = players,
	# 	time_format = TimeFormat.BLITZ,
	# )

	# previous_matchups = {p.id: [] for p in players}

	# for round_count in range(0, tournament.rounds_max):
	# 	matchups = swiss_sort(players, previous_matchups, round_count)
	# 	print(f"round {round_count + 1}:")
	# 	[print(b, w) for (b, w) in matchups]
	# 	for p in players:
	# 		p.score += randrange(30)
		# print(previous_matchups)

	# [print(p) for p in get_players()]

if __name__ == "__main__":
	main()
