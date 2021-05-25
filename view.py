#!/usr/bin/env python3

import os
import curses
import curses.textpad



KEY_ENTER = [10, 13, 343]
KEY_QUIT = ord('q')
KEY_UP = curses.KEY_UP
KEY_DOWN = curses.KEY_DOWN
KEY_LEFT = curses.KEY_LEFT
KEY_RIGHT = curses.KEY_RIGHT

DIRECTIONS = {
    KEY_UP: -1,
    KEY_DOWN: 1
}

QUIT = -1

class Win:

    def __init__(self, h, w, y, x, *args, **kwargs):
        self.win = curses.newwin(h, w, y, x)
        self.win.keypad(1)
        self.h = h
        self.w = w
        self.y = y
        self.x = x
        self.args = args
        self.kwargs = kwargs

    def draw(self):
        self.clear()
        y = 0
        for v in self.args:
            self.addstr(y, 1, v)
            y += 1
        for k, v in self.kwargs.items():
            self.addstr(y, 1, f"{k}: {v}")
        # [self.addstr(y, 1, o) for y, o in enumerate(self.args)]
        self.refresh()

    def addstr(self, y, x, s):
        self.win.addstr(y, x, s)

    def clear(self):
        self.win.clear()

    def refresh(self):
        self.win.refresh()

    def highlight_on(self, y, x, w):
        self.win.chgat(y, x, w, curses.A_REVERSE)

    def highlight_off(self, y, x, w):
        self.win.chgat(y, x, w, curses.A_NORMAL)

    def getch(self):
        return self.win.getch()


class MenuWin(Win):

    def __init__(self, h, w, y, x, *args, **kwargs):
        self.nb_opts = len(kwargs)
        self.selected = 0
        super().__init__(h, w, y, x, *args, **kwargs)

    def draw(self):
        [self.addstr(y, 1, opt) for y, opt in enumerate(self.kwargs)]

    def navigate(self):
        infos = list(self.kwargs.values())
        h = self.h
        w = os.get_terminal_size().columns - self.w - 12
        y = self.y
        x = self.w + 8
        infowin = InfoWin(h, w, y, x, *infos)
        infowin.draw(self.selected) 
        self.highlight_on(self.selected, 0, self.w)
        while True:
            c = self.getch()
            if c in [KEY_UP, KEY_DOWN]:
                self.highlight_off(self.selected, 0, self.w)
                self.selected += DIRECTIONS[c]
                self.selected %= self.nb_opts
                infowin.draw(self.selected)
                self.highlight_on(self.selected, 0, self.w)
            elif c == KEY_QUIT:
                return QUIT
            elif c in KEY_ENTER:
                self.highlight_off(self.selected, 0, self.w)
                self.refresh()
                return self.selected


class InfoWin(Win):

    def draw(self, page=0):
        self.clear()
        self.addstr(0, 0, self.args[page])
        self.refresh()


class InputWin(Win):

    def input_field(self, y, title):
        curses.textpad.rectangle(self.win, y, 0, y + 2, 32)
        self.addstr(y, 1, f" {title} ")

    def get_string(self, y):
        curses.echo()
        curses.curs_set(1)
        result = self.win.getstr(y + 1, 2, 28)
        curses.curs_set(0)
        curses.noecho()
        return str(result, 'utf-8')

    def choice_field(self, y, title, *options):
        h = len(options) + 1
        curses.textpad.rectangle(self.win, y, 0, y + h, 32)
        self.addstr(y, 1, f" {title} ")
        for i, o in enumerate(options):
            self.addstr(y + i + 1, 2, o)

    def get_choice(self, y, *options):
        selected = 0
        nb_opt = len(options)
        self.highlight_on(y + 1, 1, 31)
        while True:
            c = self.win.getch()
            if c in [KEY_DOWN, KEY_UP]:
                self.highlight_off(y + selected + 1, 1, 31)
                selected += DIRECTIONS[c]
                selected %= nb_opt
                self.highlight_on(y + selected + 1, 1, 31)
            elif c in KEY_ENTER:
                self.highlight_off(y + selected + 1, 1, 31)
                return options[selected]

    def draw(self):
        y = 0
        for f in self.args:
            if f['type'] in ["string", "date", "int"]:
                self.input_field(y, f['title'])
                y += 4
            elif f['type'] == "menu":
                self.choice_field(y, f['title'], *f['options'])
                y += len(f['options']) + 3
        self.refresh()

    def get_results(self):
        y = 0
        results = {}
        for f in self.args:
            if f['type'] in ["string", "date", "int"]:
                results[f['name']] = self.get_string(y)
                y += 4
            elif f['type'] == "menu":
                results[f['name']] = self.get_choice(y, *f['options'])
                y += len(f['options']) + 3
        return results

    def validate(self, data):
        self.clear()
        y = 0
        for entry in data:
            self.addstr(y, 0, f"{entry}: {data[entry]}")
            y += 1
        y += 2
        self.choice_field(y, "save ?", "Yes", "No")
        self.refresh()
        return (self.get_choice(y, "Yes", "No") == "Yes")


class Popup(Win):

    def __init__(self, h, w, y, x, *args, **kwargs):
        min_w = 29
        max_w = 58 #maximum line length
        self.message = [args[1][i:max_w+i] for i in range(0, len(args[1]), max_w)]
        h = len(self.message) + 3
        w = max(min_w + 4, len(self.message[0]) + 4)
        y = curses.LINES // 2 - h // 2
        x = curses.COLS // 2 - w // 2
        super().__init__(h, w, y, x, *args, **kwargs)

    def draw(self):
        self.win.box()
        self.addstr(0, 1, f" {self.args[0]} ")
        for y, line in enumerate(self.message):
            x = self.w//2 - len(line)//2
            self.addstr(y + 1, x, line)
        # self.addstr(1, 1, self.message[0])
        txt = " press any key to continue "
        self.addstr(self.h - 1, self.w//2 - len(txt)//2, txt)
        self.refresh()
        self.getch()
        self.clear()
        self.refresh()


######################################################

def init(stdscr):
    curses.curs_set(0)
    stdscr.keypad(1)
    stdscr.box()
    stdscr.refresh()


def start(func):
    curses.wrapper(func)


def stop():
    curses.curs_set(1)


if __name__ == "__main__":
    curses.wrapper(main)
