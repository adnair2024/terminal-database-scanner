import curses
from utils.db_helpers import get_table_rows, get_table_columns

class RowViewer:
    def __init__(self, stdscr, conn):
        self.stdscr = stdscr
        self.conn = conn
        self.offset = 0
        self.rows_per_page = curses.LINES - 4

    def display_table(self, table_name):
        columns = get_table_columns(self.conn, table_name)
        total_rows = get_table_rows(self.conn, table_name, limit=1000000)
        max_offset = max(0, len(total_rows) - self.rows_per_page)

        self.offset = 0
        while True:
            rows = get_table_rows(self.conn, table_name, limit=self.rows_per_page, offset=self.offset)
            self.stdscr.clear()
            self.stdscr.addstr(0, 0, f"Table: {table_name}", curses.A_BOLD)
            self.stdscr.addstr(1, 0, " | ".join(columns), curses.A_UNDERLINE)

            for idx, row in enumerate(rows):
                y = idx + 2
                row_str = " | ".join([str(r) for r in row])
                self.stdscr.addstr(y, 0, row_str[:curses.COLS-1])

            self.stdscr.addstr(curses.LINES-1, 0, "Up/Down: scroll, b: back")
            self.stdscr.refresh()

            key = self.stdscr.getch()
            if key == curses.KEY_DOWN and self.offset < max_offset:
                self.offset += 1
            elif key == curses.KEY_UP and self.offset > 0:
                self.offset -= 1
            elif key == ord("b"):
                break
