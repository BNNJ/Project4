#!/usr/bin/env python3

# import curses
import model
import view

KEY_ENTER = [10, 13, 343]
QUIT = -1


###############################################################################
# TOURNAMENT MENU
###############################################################################

TOURNAMENT_MENU = {
    'infos': "",
    'set match results': "Set the results for a match from the current round",
    'save': "save the current state of the tournament",
    'show players': "Show the players participating in the tournament",
}


def tournament_menu(h, w, tournament):
    menu = view.MenuWin(h-8, 24, 2, 2, **TOURNAMENT_MENU)
    menu.draw()
    while True:
        selected = menu.navigate()
        if selected == QUIT:
            break
        elif selected == 0:
            pass
        elif selected == 1:
            pass
        elif selected == 2:
            pass
        elif selected == 3:
            pass


###############################################################################
# MAIN MENU
###############################################################################

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
}

TOURNAMENT_FORM = [
    {
        'name': "name",
        'title': "tournament name",
        'type': "string"
    },
    {
        'name': "location",
        'title': "location",
        'type': "string"
    },
    {
        'name': "date",
        'title': "date",
        'type': "date"
    },
    {
        'name': "players",
        'title': "players",
        'type': "menu",
        'nb_choices': 8,
        'options': {}
    },
    {
        'name': "time_format",
        'title': "time format",
        'type': "select",
        'options': ["bullet", "blitz", "fast move"]
    },
    {
        'name': "description",
        'title': "description",
        'type': "long"
    }
]

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
        'type': "select",
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
    }
]


def new_tournament(h, w, y, x):
    form = TOURNAMENT_FORM
    form[3]['options'] = model.list_players()
    win = view.InputWin(h, w, y, x, *form)
    win.draw()
    results = win.get_results()
    if win.validate(results):
        tournament = model.new_tournament(**results)
        tournament.save()
        view.Popup("info", "new tournament created").draw()
        return tournament
    else:
        view.Popup("info", "tournament discarded").draw()


def load_tournament(h):
    tournament = list_tournaments(h)
    if tournament is not None:
        return model.load_tournament(tournament)


def list_tournaments(h):
    tournaments = model.list_tournaments()
    if tournaments is not None:
        win = view.MenuWin(h, 24, 2, 2, **tournaments)
        win.draw()
        selected = win.navigate()
        win.clear()
        win.refresh()
        return selected
    else:
        view.Popup("info", "No tournament in the database").draw()


def new_player(h, w, y, x):
    win = view.InputWin(h, w, y, x, *PLAYER_FORM)
    win.draw()
    results = win.get_results()
    if win.validate(results):
        model.new_player(**results).save()
        view.Popup("info", "player saved").draw()
    else:
        view.Popup("info", "player discarded").draw()


def list_players(h):
    players = model.list_players()
    if players is not None:
        win = view.MenuWin(h, 24, 2, 2, **players)
        win.draw()
        selected = win.navigate()
        win.clear()
        win.refresh()
        return selected
    else:
        view.Popup("info", "No players in the database").draw()


def controller(stdscr):
    view.init(stdscr)
    h, w = stdscr.getmaxyx()
    menu = view.MenuWin(h-8, 24, 2, 2, **MENU)
    tournament = None
    while True:
        menu.draw()
        # menu.refresh()
        selected = menu.navigate()
        if selected == QUIT:
            break
        elif selected == 0:
            if tournament is not None:
                menu.clear()
                tournament_menu(h, w, tournament)
            else:
                view.Popup("info", "No tournament selected,"
                           "load one from the database or start a new one")\
                    .draw()
        elif selected == 1:
            tournament = new_tournament(h-8, w-36, 2, 32)
        elif selected == 2:
            tournament = load_tournament(h-8)
        elif selected == 3:
            list_tournaments(h-8)
        elif selected == 4:
            new_player(h-8, w-36, 2, 32)
        elif selected == 5:
            list_players(h-8)
        elif selected == 6:
            pass
        elif selected == 7:
            view.Popup("bla", "HELLO").draw()
    view.stop()


def start(players_db, tournaments_db):
    model.start(players_db, tournaments_db)
    view.start(controller)
    # print(type(model.list_players()))
