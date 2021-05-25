#!/usr/bin/env python3

import curses
import model
import view

KEY_ENTER = [10, 13, 343]
QUIT = -1
MENU = {
    'current tournament': (
        "More options for the current tournament:\n"
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

PLAYER_FORM = [
    {
        'name': "first_name",
        'title': "first name",
        'type': "string",
    },
    {
        'name': "last_name",
        'title': "last name",
        'type': "string",
    },
    {
        'name': "gender",
        'title': "gender",
        'type': "menu",
        'options': ["Male", "Female"],
    },
    {
        'name': "birth_date",
        'title': "birth date",
        'type': "date",
    },
    {
        'name': "rank",
        'title': "rank",
        'type': "int",
    },
]

def add_player(h, w, y, x):
    win = view.InputWin(h, w, y, x, *PLAYER_FORM)
    win.draw()
    results = win.get_results()
    if win.validate(results): 
        model.new_player(**results).save()
        view.Popup(3, 30, 10, 24, "info", "player saved").draw()
    else:
        view.Popup(3, 30, 10, 24, "info", "player discarded").draw()

def list_players(h, w, y, x):
    win = view.Win(h, w, y, x, *model.list_players())
    win.draw()
    win.getch()


def controller(stdscr):
    if not view.size_check(stdscr):
        return

    view.init(stdscr)
    h, w = stdscr.getmaxyx()
    menu = view.MenuWin(h-8, 24, 2, 2, **MENU)
    menu.draw()
    while True:
        selected = menu.navigate()
        if selected == QUIT:
            break
        elif selected == 4:
            add_player(h-8, w-36, 2, 32)
            menu.draw()
        elif selected == 5:
            list_players(h-8, w-36, 2, 32)
    view.stop()


def start():
    view.start(controller)
    # print(type(model.list_players()))
