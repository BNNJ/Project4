#!/usr/bin/env python3

import curses
import curses.textpad

MENU = {
    'current tournament': (
        "More options for the current tournintament:\n"
        "* save tournament\n"
        "* register round or match\n"
        "* declare winner\n"
        "..."
    ),
    'start a tournament': "Start a new tournament",
    'load a tournament': (
        "Load a previously started tournament,"
        " from the tournament database"
    ),
    'tournament list': "Display the list of tournaments in the database",
    'add a player': "Add a new player to the database",
    'show all players': "Show all players in the database",
    'line test': "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. \n Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.", 
    # 'column test': "foobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\n",
}

t = {
	'foo': "FOO",
	'bar': "BAR",
	'hello': "HELLO",
	'world': "WORLD"
}


class Foo:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def print(self):
		print(self.x, self.y)

class Bar(Foo):
	def __init__(self, x, y):
		super().__init__(x, y)
		self.x = x+2

foo = Foo(3, 4)
