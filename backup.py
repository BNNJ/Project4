#!/usr/bin/env python3

import curses


KEY_ENTER = [10, 13, 343]
QUIT = -1


class Win:
    def __init__(self, h, w, y, x):
        self.h = h
        self.w = w
        self.win = curses.newwin(h, w, y, x)

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

    def clear(self):
        self.win.clear()

    def refresh(self):
        self.win.refresh()

    def highlight_on(self, y):
        self.win.chgat(y, 0, self.w - 25, curses.A_REVERSE)

    def highlight_off(self, y):
        self.win.chgat(y, 0, self.w - 25, curses.A_NORMAL)


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
        self.menu.highlight_on(selected)
        self.info.draw(self.infos[selected].split('\n'))
        self.refresh()

    def resize(self, h, w, selected):
        # self.menu.kill()
        self.info.kill()
        menu_width = 24
        # self.menu = Win(h - 10, menu_width, 2, 4)
        self.info = Win(h - 10, w - menu_width - 20, 2, menu_width + 12)
        self.box()
        self.draw(selected)

    def navigate(self, selected=0):
        # selected = 0
        self.menu.refresh()
        while True:
            ch = self.screen.getch()
            if ch in [curses.KEY_DOWN, curses.KEY_UP]:
                self.menu.highlight_off(selected)
                selected += 1 if ch == curses.KEY_DOWN else -1
                selected %= len(self.options)
                self.info.draw(self.infos[selected].split('\n'))
                self.menu.highlight_on(selected)
                self.refresh()
            elif ch == ord('q'):
                return QUIT
            elif ch in KEY_ENTER:
                self.menu.highlight_off(selected)
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


# def enum_kwargs(kwargs, y=0):
#     i = y
#     for k, v in kwargs.items():
#         yield i, k, v
#         i += 1


# def resize_term(win, y, x, w, selected, *options):
#     win.clear()
#     H, W = win.getmaxyx()
#     if H < 20 or W < 63:
#         win.clear()
#         addstr(win, H // 2 - 1, W, "Stop squeezing me !")
#         win.getch()
#         return
#     win.box()
#     addstr(win, 0, W, " CHESS PRO 3000 ")
#     legend = (" move with up and down arrows, select with enter, quit with q ")
#     addstr(win, H - 1, W, legend)
#     for i, opt in enumerate(options, y):
#         win.addstr(i, x, f"{opt}")
#     win.chgat(selected + y, x - 1, w, curses.A_REVERSE)
#     win.refresh()


# def addstr(win, y, w, s):
#     win.addstr(y, w // 2 - (len(s) + 1) // 2, s)


# def draw_box(win):
#     H, W = win.getmaxyx()
#     win.box()
#     addstr(win, 0, W, " CHESS PRO 3000 ")
#     legend = " move with up and down arrows, select with enter, quit with q "
#     addstr(win, H - 1, W, legend)


# def draw_menu(win, y, *options):
#     _, W = win.getmaxyx()
#     h, w = len(options), 0
#     for opt in options:
#         w = max(w, len(opt))
#     x = W // 4 - w // 2
#     w += 2

#     for i, opt in enumerate(options, y):
#         win.addstr(i, x, f"{opt}")
#     win.refresh()
#     return y, x, h, w


# def dump(win, *args, **kwargs):
#     win.clear()
#     for y, arg in enumerate(args):
#         win.addstr(y, 0, str(arg))
#     win.refresh()
#     win.getch()


# def new_win(stdscr, y, x):
#     h, w = stdscr.getmaxyx()
#     h = h - 10
#     w = w // 2 - 2
#     return curses.newwin(h, w, y, x)


# def draw_info(win, info):
#     win.clear()
#     win.box()
#     info = info.split("\n")
#     for i, d in enumerate(info):
#         win.addstr(i + 2, 2, d)
#     win.refresh()

# def navigate_menu(stdscr, menu_win, y, x, h, w, **options):
#     selected = 0
#     win.chgat(y, x - 1, w, curses.A_REVERSE)
#     info_win = new_win(stdscr, 4, )
#     infos = [o['info'] for o in options.values()]
#     draw_info(info_win, infos[0])
#     while True:
#         ch = win.getch()
#         if ch == curses.KEY_DOWN and selected < h - 1:
#             win.chgat(selected + y, x - 1, w, curses.A_NORMAL)
#             selected += 1
#             win.chgat(selected + y, x - 1, w, curses.A_REVERSE)
#             draw_info(info_win, infos[selected])
#         elif ch == curses.KEY_UP and selected > 0:
#             win.chgat(selected + y, x - 1, w, curses.A_NORMAL)
#             selected -= 1
#             win.chgat(selected + y, x - 1, w, curses.A_REVERSE)
#             draw_info(info_win, infos[selected])
#         elif ch in KEY_ENTER:
#             win.chgat(selected + y, x - 1, w, curses.A_NORMAL)
#             return list(options.keys())[selected]
#         elif ch == ord('q'):
#             return QUIT
#         elif ch == curses.KEY_RESIZE:
#             win.clear()
#             H, W = win.getmaxyx()
#             if H < 20 or W < 63:
#                 addstr(win, H // 2 - 1, W, "Stop squeezing me !")
#                 win.getch()
#             else:
#                 draw_box(win)
#                 y, x, h, w = draw_menu(win, y, *options)
#                 win.chgat(selected + y, x - 1, w, curses.A_REVERSE)
            # resize_term(win, y, x, w, selected, *options)


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
