#!/usr/bin/env python3

import curses
import model
import view

KEY_ENTER = [10, 13, 343]
QUIT = -1
MENU = [
    {
        'option': "current tournament",
        'info': ("More options for the current tournament:\n"
                 "* save tournament\n"
                 "* register round or match\n"
                 "* declare winner\n"
                 "..."),
        'action': lambda:None
    },
    {
        'option': "start a tournament",
        'info': "Start a new tournament",
        'action': lambda:None
    },
    {
        'option': "load a tournament",
        'info': ("Load a previously started tournament,"
                 " from the tournament database"),
        'action': lambda:None
    },
    {
        'option': "tournament list",
        'info': "Display the list of tournaments in the database",
        'action': lambda:None
    },
    {
        'option': "add a player",
        'info': "Add a new player to the database",
        'action': lambda:None
    },
    {
        'option': "show all players",
        'info': "Show all players in the database",
        'action': lambda:None
    },
    {
        'option': "line test",
        'info': "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. \n Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.", 
        'action': lambda:None
    },
    {
        'option': "column test",
        'info': "foobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\nfoobar\n",
        'action': lambda:None
    }
]

def add_player(chess):
    chess.info.clear()
    chess.info.input_field(0, "first name")
    chess.info.input_field(4, "last name")
    chess.info.choice_field(8, "gender", ["male", "female"])
    chess.info.input_field(13, "birth date")
    chess.info.refresh()

    p = {}
    curses.echo()
    curses.curs_set(1)
    p['first_name'] = chess.info.win.getstr(1, 1, 22)
    p['last_name'] = chess.info.win.getstr(5, 1, 22)
    curses.curs_set(0)
    p['gender'] = chess.info.get_choice(9, ["male", "female"])
    curses.curs_set(1)
    p['birth_date'] = chess.info.win.getstr(14, 1, 22)
    curses.curs_set(0)
    curses.noecho()

    chess.info.clear()
    chess.info.draw(p.values())
    # chess.info.clear()
    # chess.info.refresh()
    chess.info.choice_field(len(p) + 2, "save ?", ["yes", "no"])
    save = chess.info.get_choice(len(p) + 3, ["yes", "no"])
    chess.info.clear()
    if save == "yes":
        chess.info.addstr(2, 2, "Player saved")
    if save == "no":
        chess.info.addstr(2, 2, "Player not saved")
    chess.info.win.getch()

def controller(stdscr):
    if not view.size_check(stdscr):
        return

    view.init(stdscr)

    chess = view.ChessUi(stdscr, MENU)
    chess.draw()
    # selected = 0
    while True:
        selected = chess.navigate()
        if selected == QUIT:
            break
        elif selected == 5:
            chess.info.draw(model.get_all_players())
            chess.info.refresh()
        elif selected == 4:
            add_player(chess)
            # chess.info.form("first name", "last name", "gender")
            # chess.draw()
        else:
            MENU[selected]['action']()
    view.stop()


def start():
    view.start(controller)
    # controller(None)
