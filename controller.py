#!/usr/bin/env python3

import model
import view
from operator import attrgetter

QUIT = -1

###############################################################################
# TOURNAMENT MENU
###############################################################################


def finish_round(tournament):
    form = [
        {
            'name': i,
            'title': (
                f"{m.white.first_name} (white) "
                f"vs {m.black.first_name} (black)"
            ),
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
        view.Popup("info", "round finished, scores registered").draw()
    else:
        view.Popup("info", "scores discarded").draw()


def start_round(tournament):
    tournament.start_round()


def save_tournament(tournament):
    form = [
        {
            'name': 'save',
            'title': "save tournament ?",
            'type': "select",
            'options': ["Yes", "No"]
        }
    ]
    win = view.InputWin(INFO_H, INFO_W, 2, MENU_W + 8, *form)
    win.draw()
    if win.get_results()['save'] == "Yes":
        tournament.save()
        view.Popup("info", "tournament saved").draw()
    else:
        view.Popup("info", "tournament not saved").draw()


def show_players(tournament):
    form = [
        {
            'name': "sort_method",
            'title': "sort method",
            'type': "select",
            'options': ["alpha", "rank", "id"]
        }
    ]
    win = view.InputWin(INFO_H, INFO_W, 2, MENU_W+8, *form)
    win.draw()

    if win.get_results()['sort_method'] == "rank":
        players = sorted(tournament.players, key=attrgetter('rank'))
    else:
        players = sorted(tournament.players, key=attrgetter('last_name'))

    players = {
        f"{p.first_name} {p.last_name}": (
            f"{p.first_name} {p.last_name}\n"
            f"rank:       {p.rank}\n"
            f"score:      {p.score}\n"
            f"birth date: {p.birth_date}\n"
            f"gender:     {p.gender}"
        ) for p in players
    }
    win = view.MenuWin(MENU_H, MENU_W, 2, 2, **players)
    win.draw()
    selected = win.navigate()
    win.clear()
    win.refresh()
    return selected


def update_rank(tournament):
    selected = show_players(tournament)
    form = [
        {
            'name': "rank",
            'title': "new rank",
            'type': "int"
        }
    ]
    win = view.InputWin(INFO_W, INFO_W, 2, MENU_W + 8, *form)
    win.draw()
    results = win.get_results()
    if win.validate(results):
        tournament.players[selected].update_rank(results['rank'])
        view.Popup("info", "player rank updated").draw()
    else:
        view.Popup("info", "new player rank discarded").draw()


def update_description(tournament):
    form = [
        {
            'name': "descriptiom",
            'title': "description",
            'type': "long"
        }
    ]
    win = view.InputWin(INFO_W, INFO_W, 2, MENU_W + 8, *form)
    win.draw()
    results = win.get_results()
    if win.validate(results):
        tournament.update_description(results['description'])
        view.Popup("info", "description updated").draw()
    else:
        view.Popup("info", "new description discarded").draw()


def menu_template(tournament):
    round_states = {
        True: {"finish round": "finish round and assign results"},
        False: {"start round": "start a new round"}
    }
    template = {
        'infos': (
            f"name:          {tournament.name}\n"
            f"location:      {tournament.location}\n"
            f"current round: {tournament.round_nb}\n"
            f"date:          {tournament.date}\n"
            f"players:       {tournament.players}"
        ),
        **round_states[tournament.round_started],
        'save': "Save the current state of the tournament",
        'show players': "Show the players participating in the tournament",
        'show rounds': '\n'.join([
            (
                f"{r.name}: "
                f"{[f'{m.white._id}v{m.black._id}' for m in r.matches]}"
            ) for r in tournament.rounds
        ]),
        'show matches': '\n'.join(
            [
                (
                    f"{m.white.full_name:>22}  {m.white_score:>3}"
                    f" vs {m.black_score:<3}  {m.black.full_name :<22}"
                ) for r in tournament.rounds for m in r.matches
            ]
        ),
        'update player rank': "Update a player's rank",
        'update description': "Change the description of the tournament"
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
            show_players(tournament)
        elif selected == 4:
            pass
        elif selected == 5:
            pass
        elif selected == 6:
            update_rank(tournament)
            menu.draw()
        elif selected == 7:
            update_description(tournament)
            menu.draw()


###############################################################################
# MAIN MENU
###############################################################################


def new_tournament():
    if model.number_of_players() < 8:
        view.Popup("info", "not enough players in the database !").draw()
        return

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

    win = view.InputWin(INFO_H, INFO_W, 2, MENU_W+8, *form)
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
    if model.number_of_players() <= 0:
        view.Popup("info", "No players in the database").draw()
    else:
        form = [
            {
                'name': "sort_method",
                'title': "sort method",
                'type': "select",
                'options': ["alpha", "rank", "id"]
            }
        ]
        win = view.InputWin(INFO_H, INFO_W, 2, MENU_W+8, *form)
        win.draw()
        sort_method = win.get_results()['sort_method']

        players = model.list_players(sort_method)
        win = view.MenuWin(MENU_H, MENU_W, 2, 2, **players)
        win.draw()
        selected = win.navigate()
        win.clear()
        win.refresh()
        return selected + 1  # adjust for 1-indexed database id


def controller(stdscr):
    view.init(stdscr)
    global H, W, MENU_H, MENU_W, INFO_H, INFO_W
    H, W = stdscr.getmaxyx()
    MENU_H = H - 8
    MENU_W = 24
    INFO_H = MENU_H
    INFO_W = W - (MENU_W + 12)

    menu = {
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
        'exit': "Exit the program. Don't forget to save your stuff !"
    }

    menu = view.MenuWin(MENU_H, MENU_W, 2, 2, **menu)
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
