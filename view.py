#!/usr/bin/env python3

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

    def __init__(self, screen, h, w, y, x, data):
        self.win = curses.newwin(h, w, y, x)
        self.win.keypad(1)
        self.screen = screen
        self.h = h
        self.w = w
        self.y = y
        self.x = x
        self.data = data

    def draw(self):
        self.clear()
        [self.addstr(y, 1, o) for y, o in enumerate(self.data)]
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

    def __init__(self, screen, h, w, y, x, data):
        self.nb_opts = len(data)
        self.selected = 0
        super().__init__(screen, h, w, y, x, data)

    def navigate(self):
        infos = list(self.data.values())
        h = self.h
        _, w = self.screen.getmaxyx()
        w -= self.w + 12
        y = self.y
        x = self.w + 8
        infowin = InfoWin(self.screen, h, w, y, x, infos)
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

    def __init__(self, screen, h, w, y, x, data):
        data = [page.split('\n') for page in data]
        # self.infos = [
        #     [page[i:i+w-2] for i in range(0, len(page), w-2)]
        #     for page in infos
        # ]
        super().__init__(screen, h, w, y, x, data)

    def draw(self, page=0):
        self.clear()
        page = self.data[page]
        # [self.addstr(y, 1, s) for y, s in enumerate(page)]
        y = 0
        for line in page:
            self.addstr(y, 0, line)
            y += 1 + len(line) // self.w
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
        return str(result)

    def choice_field(self, y, title, options):
        h = len(options) + 1
        curses.textpad.rectangle(self.win, y, 0, y + h, 32)
        self.addstr(y, 1, f" {title} ")
        for i, o in enumerate(options):
            self.addstr(y + i + 1, 2, o)

    def get_choice(self, y, options):
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
        for f in self.data:
            if f['type'] in ["string", "date"]:
                self.input_field(y, f['title'])
                y += 4
            elif f['type'] == "menu":
                self.choice_field(y, f['title'], f['options'])
                y += len(f['options']) + 3
        self.refresh()

    def get_results(self):
        y = 0
        results = {}
        for f in self.data:
            if f['type'] in ["string", "date"]:
                results[f['name']] = self.get_string(y)
                y += 4
            elif f['type'] == "menu":
                results[f['name']] = self.get_choice(y, f['options'])
                y += len(f['options']) + 3
        self.clear()
        for y, entry in enumerate(results):
            self.addstr(y, 0, f"{entry}: {results[entry]}")
        y = len(results) + 2
        self.choice_field(y, "save ?", ["Yes", "No"])
        self.refresh()
        if self.get_choice(y, ["Yes", "No"]) == "yes":
            return results
        else:
            return None

    # def get_choice(self, y, options):


    # def draw_list(self, data):
    #     self.clear()
    #     h, w = self.win.getmaxyx()
    #     max_page(len(data) // h)
    #     pages = []
    #     for d in data:
    #         self.win.addstr(y, x, d)
    #         y += 1 + (len(d) // w)
    #         if y >= h - 1:
    #             x += col_width
    #             y = 0
    #         if x >= w - col_width:
    #             break
    #     return y, x, h, w

######################################################

def size_check(win):
    H, W = curses.LINES, curses.COLS
    if H < 20 or W < 63:
        addstr(win, H // 2 - 1, W, "That terminal is way too small, dude !")
        addstr(win, H // 2, W, "Press any key to quit")
        win.refresh()
        win.getch()
        return False
    return True


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
