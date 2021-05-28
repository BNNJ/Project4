#!/usr/bin/env python3

import model
import view

QUIT = -1

###############################################################################
# TOURNAMENT MENU
###############################################################################


def finish_round(tournament):
    form = [
        {
            'name': i,
            'title': f"{m.white._id} vs {m.black._id}",
            'type': "select",
            'options': ["black", "white", "draw"]
        } for i, m in enumerate(tournament.current_round.matches)
    ]
    win = view.InputWin(INFO_H, INFO_W, 2, MENU_W + 8, *form)
    win.draw()
    results = win.get_results()
    if win.validate(results):
        results = list(results.values())
        tournament.end_round(results)
        view.Popup("info", "round finished, scores registered")
    else:
        view.Popup("info", "scores discarded")


def start_round(tournament):
    tournament.start_round()
    pass
    # rnd = swiss_sort(tournament.players, )


def save_tournament(tournament):
    tournament.save()


def show_players(players):
    p = {
        f"{p.first_name} {p.last_name}": (
            f"rank:       {p.rank}\n"
            f"score:      {p.score}\n"
            f"birth date: {p.birth_date}\n"
            f"gender:     {p.gender}"
        )
        for p in players
    }
    win = view.MenuWin(MENU_H, MENU_W, 2, 2, **p)
    win.draw()
    win.navigate()
    win.clear()
    win.refresh()


def menu_template(tournament):
    round_states = {
        True: {"finish round": "finish round and assign results"},
        False: {"start round": "start a new round"}
    }
    template = {
        'infos': (
            f"name:     {tournament.name}\n"
            f"location: {tournament.location}\n"
            f"date:     {tournament.date}\n"
            f"players:  {tournament.players}"
        ),
        **round_states[tournament.round_started],
        'save': "save the current state of the tournament",
        'show players': "Show the players participating in the tournament",
    }
    return template


def tournament_menu(tournament):
    menu = view.MenuWin(MENU_H, MENU_W, 2, 2, **menu_template(tournament))
    menu.draw()
    while True:
        selected = menu.navigate()
        if selected == QUIT:
            break
        elif selected == 0:
            pass
        elif selected == 1:
            if tournament.round_started:
                finish_round(tournament)
            else:
                start_round(tournament)
            menu = view.MenuWin(MENU_H, MENU_W, 2, 2,
                                **menu_template(tournament))
            menu.draw()
        elif selected == 2:
            save_tournament(tournament)
        elif selected == 3:
            show_players(tournament.players)
            menu.draw()


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


def new_tournament():
    form = [
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
            'options': model.list_players()
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
    win = view.InputWin(INFO_H, INFO_W, 2, MENU_W+8, *form)
    win.draw()
    results = win.get_results()
    if win.validate(results):
        tournament = model.Tournament(**results)
        tournament.save()
        view.Popup("info", "new tournament created").draw()
        return tournament
    else:
        view.Popup("info", "tournament discarded").draw()
    win.clear()
    win.refresh()


def load_tournament():
    tournament = list_tournaments()
    if tournament is not None:
        return model.load_tournament(tournament)


def list_tournaments():
    tournaments = model.list_tournaments()
    if tournaments is not None:
        win = view.MenuWin(MENU_H, MENU_W, 2, 2, **tournaments)
        win.draw()
        selected = win.navigate()
        win.clear()
        win.refresh()
        return selected + 1  # adjust for 1-indexed database ids
    else:
        view.Popup("info", "No tournament in the database").draw()


def new_player():
    form = [
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

    win = view.InputWin(INFO_H, INFO_W, 2, MENU_W + 8, *form)
    win.draw()
    results = win.get_results()
    if win.validate(results):
        model.new_player(**results).save()
        view.Popup("info", "player saved").draw()
    else:
        view.Popup("info", "player discarded").draw()
    win.clear()
    win.refresh()


def list_players():
    players = model.list_players()
    if players is not None:
        win = view.MenuWin(MENU_H, MENU_W, 2, 2, **players)
        win.draw()
        selected = win.navigate()
        win.clear()
        win.refresh()
        return selected + 1  # adjust for 1-indexed database id
    else:
        view.Popup("info", "No players in the database").draw()


def controller(stdscr):
    view.init(stdscr)
    global H, W, MENU_H, MENU_W, INFO_H, INFO_W
    H, W = stdscr.getmaxyx()
    MENU_H = H - 8
    MENU_W = 24
    INFO_H = MENU_H
    INFO_W = W - (MENU_W + 12)

    menu = view.MenuWin(MENU_H, MENU_W, 2, 2, **MENU)
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
                tournament_menu(tournament)
            else:
                view.Popup("info", "No tournament selected,"
                           "load one from the database or start a new one")\
                    .draw()
        elif selected == 1:
            tournament = new_tournament()
        elif selected == 2:
            tournament = load_tournament()
        elif selected == 3:
            list_tournaments()
        elif selected == 4:
            new_player()
        elif selected == 5:
            list_players()
    view.stop()


def start(players_db, tournaments_db):
    model.start(players_db, tournaments_db)
    view.start(controller)
