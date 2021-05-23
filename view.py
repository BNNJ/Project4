#!/usr/bin/env python3

import curses
import curses.textpad


KEY_ENTER = [10, 13, 343]
QUIT = -1


class Win:
    def __init__(self, h, w, y, x):
        self.h = h
        self.w = w
        self.win = curses.newwin(h, w, y, x)
        self.win.keypad(1)

    # def resize(self, h, w, y, x):
    #     self.h = h
    #     self.w = w
    #     self.y = y
    #     self.x = x
    #     del self.win
    #     self.win = curses.newwin(h, w, y, x)

    def draw(self, data):
        self.clear()
        # for i, line in enumerate(data):
        #     self.win.addstr(i, 1, line)

        y, x, h, w = 0, 1, *self.win.getmaxyx()
        col_width = 0
        for d in data:
            col_width = max(col_width, len(d))
        col_width += 2
        for d in data:
            self.win.addstr(y, x, d)
            y += 1 + (len(d) // w)
            # if len(d) >= w:
            #     y += 1
            if y >= h - 1:
                x += col_width
                y = 0
            if x >= w - col_width:
                break

        return y, x, h, w

    def kill(self):
        del self.win

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

    def input_field(self, y, title):
        curses.textpad.rectangle(self.win, y, 0, y + 2, 24)
        self.addstr(y, 1, f" {title} ")

    def choice_field(self, y, title, options):
        h = len(options) + 1
        curses.textpad.rectangle(self.win, y, 0, y + h, 24)
        self.addstr(y, 1, f" {title} ")
        for i, o in enumerate(options):
            self.addstr(y + i + 1, 1, o)

    def get_choice(self, y, options):
        self.highlight_on(y, 1, 22)
        num_choices = len(options)
        selected = 0
        while True:
            ch = self.win.getch()
            if ch == curses.KEY_DOWN and selected < num_choices - 1:
                self.highlight_off(y + selected, 1, 22)
                selected += 1
                self.highlight_on(y + selected, 1, 22)
            elif ch == curses.KEY_UP and selected > 0:
                self.highlight_off(y + selected, 1, 22)
                selected -= 1
                self.highlight_on(y + selected, 1, 22)
            elif ch in KEY_ENTER:
                self.highlight_off(y + selected, 1, 22)
                return options[selected]

    def form(self, *fields):
        self.clear()
        for i, f in enumerate(fields):
            curses.textpad.rectangle(self.win, i * 5 , 0, i * 5 + 2, 24)
            self.addstr(i * 5, 1, f" {f} ")

        results = {}

        curses.echo()
        curses.curs_set(1)
        for i, f in enumerate(fields):
            results[f] = str(self.win.getstr(i * 5 + 1, 1, 22))
        curses.noecho()
        curses.curs_set(0)

        self.clear()
        self.draw([f"{k}: {str(v)}" for k, v in results.items()])
        self.addstr(len(results) + 2, 2, "save ? y/n")
        self.refresh()
        while True:
            ch = self.win.getkey()
            self.clear()
            if ch in ['y', 'Y']:
                self.addstr(2, 2, "Saved !")
                break
            elif ch in ['n', 'N']:
                self.addstr(2, 2, "Not saved")
                break
        self.win.getch()
        return results


class ChessUi:
    def __init__(self, screen, menu):
        self.screen = screen
        self.box()
        self.options = [o['option'] for o in menu]
        self.infos = [o['info'] for o in menu]
        self.actions = [o['action'] for o in menu]
        
        h, w = screen.getmaxyx()
        menu_width = 24

        self.menu = Win(h - 5, menu_width, 2, 4)
        self.info = Win(h - 5, w - menu_width - 20, 2, menu_width + 12)

    def refresh(self):
        self.screen.noutrefresh()
        self.menu.win.noutrefresh()
        self.info.win.noutrefresh()
        curses.doupdate()

    def box(self):
        h, w = self.screen.getmaxyx()
        w = w // 2
        title = " CHESS PRO 3000 "
        legend = (" move with up and down arrows,"
                  " select with enter, quit with q ")
        self.screen.box()
        self.screen.addstr(0, w - len(title) // 2 - 1, title)
        self.screen.addstr(h - 1, w - len(legend) // 2 - 1, legend)

    def clear(self):
        self.screen.clear()
        self.menu.clear()
        self.info.clear()

    def draw(self, selected=0):
        self.menu.draw(self.options)
        self.menu.highlight_on(selected, 0, self.info.w - 25)
        self.info.draw(self.infos[selected].split('\n'))
        self.refresh()

    def resize(self, h, w, selected):
        # self.menu.kill()
        # self.info.kill()
        menu_width = 24
        # self.menu = Win(h - 10, menu_width, 2, 4)
        # self.info = Win(h - 10, w - menu_width - 20, 2, menu_width + 12)
        self.info.win.resize(h - 10, w - menu_width - 20)
        self.box()
        self.draw(selected)

    def navigate(self, selected=0):
        # selected = 0
        self.menu.refresh()
        while True:
            ch = self.screen.getch()
            if ch in [curses.KEY_DOWN, curses.KEY_UP]:
                self.menu.highlight_off(selected, 0, self.info.w - 25)
                selected += 1 if ch == curses.KEY_DOWN else -1
                selected %= len(self.options)
                self.info.draw(self.infos[selected].split('\n'))
                self.menu.highlight_on(selected, 0, self.info.w - 25)
                self.refresh()
            elif ch == ord('q'):
                return QUIT
            elif ch in KEY_ENTER:
                self.menu.highlight_off(selected, 0, self.info.w - 25)
                return selected
            elif ch == curses.KEY_RESIZE:
                self.clear()
                h, w = self.screen.getmaxyx()
                if h < 20 or w < 68:
                    self.screen.addstr(h // 2 - 1, w // 2 - 10,
                                       "Stop squeezing me !")
                    self.screen.getch()
                else:
                    self.resize(h, w, selected)


def getch(win):
    return win.getch()


def size_check(win):
    H, W = curses.LINES, curses.COLS
    if H < 20 or W < 63:
        addstr(win, H // 2 - 1, W, "That terminal is way too small, dude !")
        addstr(win, H // 2, W, "Press any key to quit")
        win.refresh()
        win.getch()
        return False
    return True


def init(win):
    curses.curs_set(0)
    win.keypad(1)


def start(func):
    curses.wrapper(func)


def stop():
    curses.curs_set(1)


if __name__ == "__main__":
    curses.wrapper(main)
