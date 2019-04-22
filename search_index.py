import curses

from schema import Schema
import search.interface

INDEX_DIR = 'catalogue_indices'


def main(stdscr):
    interface = search.interface.Interface(stdscr, INDEX_DIR, Schema.schema())
    while True:
        interface.handle_input()


curses.wrapper(main)
