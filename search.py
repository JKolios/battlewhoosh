import curses
from curses.textpad import Textbox
import signal
import sys

import whoosh.index
from whoosh.qparser import QueryParser

from schema import Schema

INDEX_DIR = 'indices'

SEARCH_PROMPT_COORDS = [0, 0]
SEARCH_PROMPT_HEIGHT = 1
SEARCH_PROMPT_WIDTH = 40

RESULT_PROMPT_COORDS = [1, 0]
RESULT_PROMPT_HEIGHT = 60
RESULT_PROMPT_WIDTH = 100


def get_index(directory=INDEX_DIR):
    return whoosh.index.open_dir(directory, readonly=True, schema=Schema)


def search(index, default_attribute, query_string, max_results=None):
    with index.searcher() as searcher:
        query_parser = QueryParser(default_attribute, schema=Schema.schema())
        query = query_parser.parse(query_string)
        search_hits = searcher.search(query, limit=max_results)
        return [hit.fields() for hit in search_hits]


def init_search_window():
    search_win = curses.newwin(
        SEARCH_PROMPT_HEIGHT,
        SEARCH_PROMPT_WIDTH,
        SEARCH_PROMPT_COORDS[0],
        SEARCH_PROMPT_COORDS[1]
    )

    search_win.refresh()

    return search_win


def init_result_window():
    result_win = curses.newwin(
        RESULT_PROMPT_HEIGHT,
        RESULT_PROMPT_WIDTH,
        RESULT_PROMPT_COORDS[0],
        RESULT_PROMPT_COORDS[1]
    )

    result_win.addstr(0, 0, "Result Window!")
    result_win.refresh()

    return result_win


def results_to_string(results):
    result_rows = [hit_to_string(hit) for hit in results]
    return '\n'.join(result_rows)


def hit_to_string(hit):
    return f'{hit["name"]} {hit["game"]} {hit["document_type"]}: {hit["faction"]}'


def main(stdscr):

    search_index = get_index()
    search_window = init_search_window()
    result_window = init_result_window()

    search_window_contents = ''

    stdscr.clear()
    while True:
        search_window_key = search_window.getkey()
        if search_window_key in ('KEY_BACKSPACE', '\b', '\x7f'):
            search_window_contents = search_window_contents[:-1]
        else:
            search_window_contents += search_window_key
        search_window.clear()
        search_window.addstr(
            SEARCH_PROMPT_COORDS[0], SEARCH_PROMPT_COORDS[1], search_window_contents)
        result_window.clear()
        search_results = search(search_index, 'name',
                                search_window_contents, max_results=50)
        result_window.addstr(
            RESULT_PROMPT_COORDS[0], RESULT_PROMPT_COORDS[1], results_to_string(search_results))
        result_window.refresh()


curses.wrapper(main)
