#!/usr/bin/env python3

import curses
import curses.textpad


KEY_ENTER = [10, 13, 343]
KEY_QUIT = ord('q')
KEY_UP = curses.KEY_UP
KEY_DOWN = curses.KEY_DOWN
KEY_LEFT = curses.KEY_LEFT
KEY_RIGHT = curses.KEY_RIGHT

QUIT = -1

class Win:
    def __init__(self, screen, h, w, y, x):
        self.screen = screen
        self.win = curses.newwin(h, w, y, x)
        self.h = h
        self.w = w
        self.y = y
        self.x = x
        self.win.keypad(1)

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
    directions = {
        KEY_UP: -1,
        KEY_DOWN: 1
    }

    def __init__(self, screen, h, w, y, x, options, infos=None):
        self.options = options
        self.nb_opts = len(options)
        self.infos = infos
        self.selected = 0
        super().__init__(screen, h, w, y, x)

    def draw(self):
        self.clear()
        [self.addstr(y, 1, o) for y, o in enumerate(self.options)]
        self.refresh()

    def navigate(self):
        if self.infos is not None:
            h = self.h
            _, w = self.screen.getmaxyx()
            w -= self.w + 12
            y = self.y
            x = self.w + 8
            infowin = InfoWin(self.screen, h, w, y, x, self.infos)
            infowin.draw(self.selected) 
        self.highlight_on(self.selected, 0, self.w)
        while True:
            c = self.getch()
            if c in [KEY_UP, KEY_DOWN]:
                self.highlight_off(self.selected, 0, self.w)
                self.selected += self.directions[c]
                self.selected %= self.nb_opts
                if self.infos is not None:
                    infowin.draw(self.selected)
                self.highlight_on(self.selected, 0, self.w)
            elif c == KEY_QUIT:
                return QUIT
            elif c in KEY_ENTER:
                self.highlight_off(self.selected, 0, self.w)
                self.refresh()
                return self.selected


class InfoWin(Win):
    def __init__(self, screen, h, w, y, x, infos):
        self.infos = [page.split('\n') for page in infos]
        # self.infos = [
        #     [page[i:i+w-2] for i in range(0, len(page), w-2)]
        #     for page in infos
        # ]
        super().__init__(screen, h, w, y, x)

    def draw(self, page=0):
        self.clear()
        page = self.infos[page]
        # [self.addstr(y, 1, s) for y, s in enumerate(page)]
        y = 0
        for line in page:
            self.addstr(y, 0, line)
            y += 1 + len(line) // self.w
        self.refresh()


class InputWin(Win):
    def __init__(self, screen, h, w, y, x, inputs):
        self.inputs = inputs
        super().__init__(screen, h, w, y, x)


    # def input_field(self, y, x, title):
    #     curses.textpad.rectangle(self.win, y, x, y + 2, 24)
    #     self.addstr(y, x + 2, f" {title} ")

    # def choice_field(self, y, title, options):
    #     h = len(options) + 1
    #     curses.textpad.rectangle(self.win, y, 0, y + h, 24)
    #     self.addstr(y, 1, f" {title} ")
    #     for i, o in enumerate(options):
    #         self.addstr(y + i + 1, 1, o)

    # def get_choice(self, y, options):
    #     self.highlight_on(y, 1, 22)
    #     num_choices = len(options)
    #     selected = 0
    #     while True:
    #         ch = self.win.getch()
    #         if ch == curses.KEY_DOWN and selected < num_choices - 1:
    #             self.highlight_off(y + selected, 1, 22)
    #             selected += 1
    #             self.highlight_on(y + selected, 1, 22)
    #         elif ch == curses.KEY_UP and selected > 0:
    #             self.highlight_off(y + selected, 1, 22)
    #             selected -= 1
    #             self.highlight_on(y + selected, 1, 22)
    #         elif ch in KEY_ENTER:
    #             self.highlight_off(y + selected, 1, 22)
    #             return options[selected]


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
