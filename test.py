#!/usr/bin/env python3

import curses
import curses.textpad

KEY_ENTER = [10, 13, 343]

def input_field(win, y, x, title, max_len):
	curses.textpad.rectangle(win, y, x, y + 2, x + max_len + 2)
	win.addstr(y, x + 1, f" {title} ")
	curses.echo()
	txt = win.getstr(y + 1, x + 1, max_len)
	curses.noecho()
	return txt

def main(stdscr):
	txt = input_field(stdscr, 3, 3, "HELLO THIS IS FORM", 20)
	stdscr.addstr(10, 10, txt)
	stdscr.getch()

curses.wrapper(main)

# t = {'foo': "hello", 'bar': "WORLD"}

# def test(foo, bar):
# 	print (bar, foo)

# test(**t)