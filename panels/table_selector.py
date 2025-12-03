import curses

class TableSelector:
    def __init__(self, stdscr, tables, conn):
        self.stdscr = stdscr
        self.tables = tables
        self.conn = conn
        self.current_row = 0
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)

        # Precompute total number of rows across the entire DB
        self.total_rows = self._count_total_rows()

    def _count_total_rows(self):
        cursor = self.conn.cursor()
        total = 0
        for t in self.tables:
            cursor.execute(f"SELECT COUNT(*) FROM {t}")
            total += cursor.fetchone()[0]
        return total

    def navigate(self):
        while True:
            self.stdscr.clear()
            h, w = self.stdscr.getmaxyx()

            self.stdscr.addstr(0, 0, "Tables:", curses.A_BOLD | curses.A_UNDERLINE)

            for idx, t in enumerate(self.tables):
                y = idx + 2
                if y >= h - 2:  # make space for row count + footer
                    break
                if idx == self.current_row:
                    self.stdscr.attron(curses.color_pair(1))
                    self.stdscr.addstr(y, 0, t)
                    self.stdscr.attroff(curses.color_pair(1))
                else:
                    self.stdscr.addstr(y, 0, t)

            # === NEW: show total rows in entire database ===
            self.stdscr.addstr(h - 2, 0,
                f"{self.total_rows} rows of data in this database",
                curses.A_BOLD
            )
            self.stdscr.clrtoeol()

            # Footer
            self.stdscr.addstr(h - 1, 0, "Use arrow keys, Enter to select, q to quit")
            self.stdscr.clrtoeol()

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
