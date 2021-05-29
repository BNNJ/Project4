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
KEY_BACK = [curses.KEY_BACKSPACE, ord('\b'), ord('\x7f')]

DIRECTIONS = {
    KEY_UP: -1,
    KEY_DOWN: 1,
    KEY_LEFT: -1,
    KEY_RIGHT: 1
}

QUIT = -1


###############################################################################
# Window class
###############################################################################


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
        self.refresh()

    def addstr(self, y, x, s):
        self.win.addstr(y, x, s)

    def move(self, y, x):
        self.win.move(y, x)

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

    def __init__(self, h, w, y, x, **kwargs):
        self.nb_opts = len(kwargs)
        self.selected = 0
        self.max_lines = h - 4
        self.options = [
            list(kwargs)[i:i+self.max_lines]
            for i in range(0, len(kwargs), self.max_lines)
        ]
        self.infos = list(kwargs.values())
        super().__init__(h, w, y, x)

    def update_infos(self, key, value):
        options = []
        [options.extend(p) for p in self.options]
        self.infos[options.index(key)] = value

    def draw(self, page=0):
        [self.addstr(y, 1, o) for y, o in enumerate(self.options[page])]
        nb_lines = len(self.options[0])
        if nb_lines > self.max_lines:
            total = len()
            left_arrow = "<" if page > 0 else " "
            right_arrow = ">" if page < total else " "
            self.addstr(self.h-1, 2,
                        f"{left_arrow} {page:02d}/{total:02d} {right_arrow}")
        # self.refresh()

    def navigate(self):
        h = self.h
        w = os.get_terminal_size().columns - self.w - 12
        y = self.y
        x = self.w + 8
        infowin = InfoWin(h, w, y, x, *self.infos)
        infowin.draw(self.selected)
        self.highlight_on(self.selected, 0, self.w)
        page = 0
        page_max = len(self.options) - 1
        while True:
            c = self.getch()
            if c in [KEY_UP, KEY_DOWN]:
                self.highlight_off(self.selected, 0, self.w)
                self.selected += DIRECTIONS[c]
                self.selected %= len(self.options[page])
                infowin.draw(self.selected)
                self.highlight_on(self.selected, 0, self.w)
            elif c == KEY_LEFT and page > 0:
                page -= 1
                self.clear()
                self.draw(page)
                self.selected = 0
                self.highlight_on(self.selected, 0, self.w)
            elif c == KEY_RIGHT and page < page_max:
                page += 1
                self.clear()
                self.draw(page)
                self.selected = 0
                self.highlight_on(self.selected, 0, self.w)
            elif c == KEY_QUIT:
                return QUIT
            elif c in KEY_ENTER:
                self.highlight_off(self.selected, 0, self.w)
                self.refresh()
                return self.selected + page*(self.max_lines)


class InfoWin(Win):

    def draw(self, page=0):
        self.clear()
        self.addstr(0, 0, self.args[page])
        self.refresh()


class InputWin(Win):

    input_len = 40

    def __init__(self, y, x, h, w, *args):
        self.results = {}
        super().__init__(y, x, h, w, *args)

    def input_field(self, y, title, data):
        curses.textpad.rectangle(self.win, y, 0, y + 2, self.input_len + 2)
        self.addstr(y, 1, f" {title} ")
        self.addstr(y+1, 2, data)

    # def get_string(self, y):
    #     curses.echo()
    #     curses.curs_set(1)
    #     result = self.win.getstr(y + 1, 2, 28)
    #     curses.curs_set(0)
    #     curses.noecho()
    #     return str(result, 'utf-8')

    def get_string(self, y):
        curses.curs_set(1)
        buff = ""
        y += 1
        x = 2
        self.move(y, x)
        while True:
            c = self.getch()
            if c in KEY_ENTER:
                if buff == "":
                    buff = "0"
                break
            elif c in KEY_BACK:
                if x > 2:
                    buff = buff[:-1]
                    x -= 1
                    self.addstr(y, x, " ")
                    self.move(y, x)
            elif x == self.input_len:
                pass
            else:
                buff += chr(c)
                self.win.addstr(chr(c))
                x += 1
        curses.curs_set(0)
        return buff

    def get_int(self, y):
        curses.curs_set(1)
        buff = ""
        y += 1
        x = 2
        self.move(y, x)
        while True:
            c = self.getch()
            if c in KEY_ENTER:
                if buff == "":
                    buff = "0"
                break
            elif c in KEY_BACK:
                if x > 2:
                    buff = buff[:-1]
                    x -= 1
                    self.addstr(y, x, " ")
                    self.move(y, x)
            elif x == self.input_len:
                pass
            elif ord('0') <= c <= ord('9'):
                buff += chr(c)
                self.win.addstr(chr(c))
                x += 1
        curses.curs_set(0)
        return buff

    def date_field(self, y, title, data):
        curses.textpad.rectangle(self.win, y, 0, y + 2, 13)
        self.addstr(y, 1, f" {title} ")
        self.addstr(y + 1, 2, data)

    def get_date(self, y):
        curses.curs_set(1)
        buff = ""
        y += 1
        x = 2
        self.move(y, x)
        while True:
            c = self.getch()
            if c in KEY_ENTER:
                if date_is_valid(buff):
                    break
                else:
                    buff = ""
                    Popup("info", "Invalid date !").draw()
                    self.draw()
                    self.refresh()
                    x = 2
                    self.move(y, x)
            elif c in KEY_BACK:
                buff = buff[:-1]
                if 2 < x < 13:
                    x -= 1
                if x in [4, 7]:
                    x -= 1
                self.addstr(y, x, " ")
                self.move(y, x)
            elif x == 12:
                pass
            elif ord('0') <= c <= ord('9'):
                buff += chr(c)
                self.win.addstr(chr(c))
                x += 1
                if x in [4, 7]:
                    x += 1
                self.move(y, x)
        curses.curs_set(0)
        return f"{buff[:2]}/{buff[2:4]}/{buff[4:8]}"

    def long_field(self, y, title, data):
        curses.textpad.rectangle(self.win, y, 0, y+7, self.input_len+2)
        self.addstr(y, 1, f" {title} ")
        txt = [
            data[i:i+self.input_len-2]
            for i in range(0, len(data), self.input_len-2)
        ]
        for y, line in enumerate(txt):
            self.addstr(y+1, 2, line)

    def get_long(self, y):
        curses.curs_set(1)
        txt = ""
        start_y = y + 1
        y, x = 0, 2
        self.move(start_y, 2)
        while True:
            c = self.getch()
            if c in KEY_ENTER:
                break
            elif c in KEY_BACK:
                txt = txt[:-1]
                if x > 2:
                    x -= 1
                elif y > 0:
                    x = self.input_len
                    y -= 1
                self.addstr(start_y+y, x, " ")
            elif x >= self.input_len and y >= 5:
                pass
            elif 32 <= c <= 126:
                txt += chr(c)
                self.win.addstr(chr(c))
                if x < self.input_len:
                    x += 1
                else:
                    x = 2
                    y += 1
            self.move(start_y+y, x)
        curses.curs_set(0)
        return txt

    def select_field(self, y, title, *options):
        h = len(options) + 1
        curses.textpad.rectangle(self.win, y, 0, y+h, self.input_len+2)
        self.addstr(y, 1, f" {title} ")
        for i, o in enumerate(options):
            self.addstr(y+i+1, 2, o)

    def get_selection(self, y, *options):
        selected = 0
        nb_opt = len(options)
        self.highlight_on(y + 1, 1, self.input_len+1)
        while True:
            c = self.win.getch()
            if c in [KEY_DOWN, KEY_UP]:
                self.highlight_off(y + selected + 1, 1, self.input_len+1)
                selected += DIRECTIONS[c]
                selected %= nb_opt
                self.highlight_on(y + selected + 1, 1, self.input_len+1)
            elif c in KEY_ENTER:
                self.highlight_off(y + selected + 1, 1, self.input_len+1)
                return options[selected]

    def get_menu(self, y, nb_choices, **options):
        menu = MenuWin(self.h, 24, 2, 2, **options)
        menu.draw()
        self.highlight_on(y+1, 1, self.input_len+1)
        self.getch()

        players = []
        while len(players) < nb_choices:
            selected = menu.navigate() + 1  # adjust for 1-indexed database id
            if selected in players:
                Popup("error", "This player is already in the selected pool")\
                    .draw()
            else:
                players.append(selected)
                Popup("info", f"{len(players)}/{nb_choices} players selected")\
                    .draw()

        menu.clear()
        menu.refresh()

        self.highlight_off(y+1, 1, self.input_len+1)
        self.draw()
        return players

    def draw(self):
        y = 0
        for f in self.args:
            if f['type'] in ["string", "int"]:
                self.input_field(y, f['title'],
                                 self.results.get(f['name'], ""))
                y += 4
            elif f['type'] == "date":
                self.date_field(y, f['title'],
                                self.results.get(f['name'], "  /  /    "))
                y += 4
            elif f['type'] == "long":
                self.long_field(y, f['title'], self.results.get(f['name'], ""))
                y += 8
            elif f['type'] == "select":
                self.select_field(y, f['title'], *f['options'])
                y += len(f['options']) + 3
            elif f['type'] == "menu":
                self.input_field(y, f['title'], "press a key to access menu")
                y += 4
        self.refresh()

    def get_results(self):
        y = 0
        for f in self.args:
            if f['type'] == "string":
                self.results[f['name']] = self.get_string(y)
                y += 4
            elif f['type'] == "int":
                self.results[f['name']] = self.get_int(y)
                y += 4
            elif f['type'] == "date":
                self.results[f['name']] = self.get_date(y)
                y += 4
            elif f['type'] == "long":
                self.results[f['name']] = self.get_long(y)
                y += 8
            elif f['type'] == "select":
                self.results[f['name']] = self.get_selection(y, *f['options'])
                y += len(f['options']) + 3
            elif f['type'] == "menu":
                self.results[f['name']] = self.get_menu(y, f['nb_choices'],
                                                        **f['options'])
                y += 4
        return self.results

    def validate(self, data):
        self.clear()
        y = 0
        for entry in data:
            self.addstr(y, 0, f"{entry}: {data[entry]}")
            y += 1
        y += 4
        self.select_field(y, "save ?", "Yes", "No")
        self.refresh()
        return (self.get_selection(y, "Yes", "No") == "Yes")


class Popup(Win):

    def __init__(self, *args, **kwargs):
        min_w = 29
        max_len = 58
        self.message = [
            args[1][i:max_len+i] for i in range(0, len(args[1]), max_len)
        ]
        h = len(self.message) + 3
        w = max(min_w + 4, len(self.message[0]) + 4)
        y = curses.LINES // 2 - h // 2
        x = curses.COLS // 2 - w // 2
        super().__init__(h, w, y, x, args[0])

    def draw(self):
        self.win.box()
        self.addstr(0, 1, f" {self.args[0]} ")
        for y, line in enumerate(self.message):
            x = self.w//2 - len(line)//2
            self.addstr(y + 1, x, line)
        txt = " press any key to continue "
        self.addstr(self.h - 1, self.w//2 - len(txt)//2, txt)
        self.refresh()
        self.getch()
        self.clear()
        self.refresh()


###############################################################################

def leap_year(y):
    if y % 4 != 0:
        return False
    elif y % 100 != 0:
        return True
    elif y % 400 != 0:
        return False
    else:
        return True


def date_is_valid(d):
    if (len(d) != 8):
        return False
    day = int(d[:2])
    month = int(d[2:4])
    year = int(d[4:8])

    if (month <= 0) or (month > 12):
        return False
    elif (month == 2) and (not leap_year(year)) and (day > 28):
        return False
    elif (month == 2) and (day > 29):
        return False
    elif (month in [4, 6, 9, 11]) and day > 30:
        return False
    elif day > 31:
        return False
    else:
        return True


def init(stdscr):
    curses.curs_set(0)
    stdscr.keypad(1)
    stdscr.box()
    h, w = stdscr.getmaxyx()
    title = " SUPER CHESS PRO ORGANIZER 3000 "
    stdscr.addstr(0, w//2 - len(title)//2, title)
    info = " arrow keys to navigate, enter to select, q to quit "
    stdscr.addstr(h-1, w//2 - len(info)//2, info)
    stdscr.refresh()


def start(func):
    curses.wrapper(func)


def stop():
    curses.curs_set(1)
