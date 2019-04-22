import curses

from search.context import SearchContext
from search.result_window import ResultWindow
from search.term_window import TermWindow

STATE_TRANSITIONS = {
    'search': 'details',
    'details': 'search'
}

MAX_RESULT_LINES = 40


class Interface:

    def __init__(self, curses_screen, index_dir, schema):
        self.search_context = SearchContext(index_dir, schema)
        self.result_window = ResultWindow(max_lines=MAX_RESULT_LINES)
        self.term_window = TermWindow()
        self.screen = curses_screen
        self.key_handlers = {
            'KEY_BACKSPACE': self.clear_last_term_char,
            '\b': self.clear_last_term_char,
            '\x7f': self.clear_last_term_char,
            '\x1b': self.quit_handler,
            'KEY_UP': self.move_highlight_up,
            'KEY_DOWN': self.move_highlight_down,
            '\n': self.toggle_details,
            'KEY_RESIZE': self.refresh_results,
        }

        self.state = 'search'
        self.search_term = ''
        self.search_results = []
        self.highlighted_line = -1

        self.screen.leaveok(0)
        self.screen.keypad(1)
        curses.curs_set(0)

    def handle_input(self):
        incoming_key = self.screen.getkey()
        if self.is_search_term_char(incoming_key):
            self.add_key_to_term(incoming_key)
            return
        self.key_handlers.get(incoming_key, self.no_op)()

    def run_search(self, term):
        return self.search_context.search(['name', 'document_type'], term, max_results=MAX_RESULT_LINES)

    def search_and_display(self):
        self.term_window.show_search_term(self.search_term)
        self.search_results = self.run_search(self.search_term)
        self.result_window.show_results(self.search_results)
    
    def refresh_results(self):
        self.term_window.show_search_term(self.search_term)
        self.result_window.show_results(self.search_results)

    def add_key_to_term(self, key):
        if self.state == 'search':
            self.search_term += (key)
            self.highlighted_line = -1
            self.search_and_display()

    def clear_last_term_char(self):
        if self.state == 'search':
            self.search_term = self.search_term[:-1]
            self.highlighted_line = -1
            self.search_and_display()

    def move_highlight_up(self):
        if self.highlighted_line > 0 and self.state == 'search':
            self.clear_highlight()
            self.highlighted_line -= 1
            self.result_window.highlight_line(self.highlighted_line)

    def move_highlight_down(self):
        if self.highlighted_line < len(self.search_results)-1 and self.state == 'search':
            self.clear_highlight()
            self.highlighted_line += 1
            self.result_window.highlight_line(self.highlighted_line)

    def clear_highlight(self):
        if self.highlighted_line >= 0:
            self.result_window.unhighlight_line(self.highlighted_line)

    def toggle_details(self):
        self.state = STATE_TRANSITIONS[self.state]
        if self.state == 'search':
            self.highlighted_line = -1
            self.result_window.show_results(self.search_results)
        else:
            self.result_window.show_details(
                self.search_results[self.highlighted_line])

    def quit_handler(self):
        quit(0)

    def no_op(self):
        pass

    @staticmethod
    def is_search_term_char(key):
        return (key.isalnum() or key == ' ') and len(key) == 1
