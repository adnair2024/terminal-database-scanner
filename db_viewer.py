#!/usr/bin/env python3
import curses
from pathlib import Path
import sys
from utils.db_helpers import get_db_tables, connect_db
from panels.table_selector import TableSelector
from panels.row_viewer import RowViewer

def select_db(stdscr, directory):
    db_files = [f.name for f in Path(directory).glob("*.db")]
    if not db_files:
        stdscr.addstr(0, 0, "No .db files found in this directory. Press any key to exit.")
        stdscr.getch()
        return None

    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)
    current_row = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Select a database (.db)", curses.A_BOLD | curses.A_UNDERLINE)
        for idx, f in enumerate(db_files):
            y = idx + 2
            if idx == current_row:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, 0, f)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, 0, f)
        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(db_files) - 1:
            current_row += 1
        elif key == ord("\n"):
            return Path(directory) / db_files[current_row]
        elif key == ord("q"):
            return None

def main(stdscr, directory):
    db_file = select_db(stdscr, directory)
    if not db_file:
        return

    conn = connect_db(db_file)
    tables = get_db_tables(conn)
    if not tables:
        stdscr.addstr(0, 0, f"No tables found in {db_file}. Press any key to exit.")
        stdscr.getch()
        return

    table_selector = TableSelector(stdscr, tables, conn)
    row_viewer = RowViewer(stdscr, conn)

    while True:
        selected_table = table_selector.navigate()
        if selected_table is None:
            break
        row_viewer.display_table(selected_table)

    conn.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python db_viewer.py <directory>")
        sys.exit(1)
    curses.wrapper(main, sys.argv[1])
