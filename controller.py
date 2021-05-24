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
    h, w = stdscr.getmaxyx()
    menu = view.MenuWin(stdscr, h-8, 24, 2, 2, MENU)
    menu.draw()
    while True:
        selected = menu.navigate()
        if selected == QUIT:
            break
        elif selected == 4:
            win = view.InputWin(stdscr, h-8, w-36, 2, 32, PLAYER_FORM)
            win.draw()
            results = win.get_results()
            if win.validate(results): 
                model.new_player(**results).save()
                view.Popup(stdscr, 5, 30, 10, 10, ["info", "player saved"]).draw()
                # pop.draw()
                # pop.clear()
                # del pop
                stdscr.clear()
                stdscr.box()
                stdscr.refresh()
                menu.draw()
        elif selected == 5:
            win = view.Win(stdscr, h-8, w-36, 2, 32, model.list_players())
            win.draw()
            win.getch()
    view.stop()


def start():
    view.start(controller)
    # print(type(model.list_players()))
