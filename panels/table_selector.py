import curses

class TableSelector:
    def __init__(self, stdscr, tables):
        self.stdscr = stdscr
        self.tables = tables
        self.current_row = 0
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)

    def navigate(self):
        while True:
            self.stdscr.clear()
            h, w = self.stdscr.getmaxyx()
            self.stdscr.addstr(0, 0, "Tables:", curses.A_BOLD | curses.A_UNDERLINE)
            for idx, t in enumerate(self.tables):
                y = idx + 2
                if y >= h - 1:
                    break
                if idx == self.current_row:
                    self.stdscr.attron(curses.color_pair(1))
                    self.stdscr.addstr(y, 0, t)
                    self.stdscr.attroff(curses.color_pair(1))
                else:
                    self.stdscr.addstr(y, 0, t)
            self.stdscr.addstr(h-1, 0, "Use arrow keys, Enter to select, q to quit")
            self.stdscr.refresh()

            key = self.stdscr.getch()
            if key == curses.KEY_UP and self.current_row > 0:
                self.current_row -= 1
            elif key == curses.KEY_DOWN and self.current_row < len(self.tables) - 1:
                self.current_row += 1
            elif key == ord("\n"):
                return self.tables[self.current_row]
            elif key == ord("q"):
                return None
