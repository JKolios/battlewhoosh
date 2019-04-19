import curses

class TermWindow:

    TERM_WINDOW_COORDS = [0, 0]
    TERM_WINDOW_HEIGHT = 1
    TERM_WINDOW_WIDTH = 80


    def __init__(self):
        self.window = curses.newwin(
            self.TERM_WINDOW_HEIGHT,
            self.TERM_WINDOW_WIDTH,
            self.TERM_WINDOW_COORDS[0],
            self.TERM_WINDOW_COORDS[1]
        )
        self.window.immedok(True)

    def show_search_term(self, term):
        self.window.erase()
        self.window.addnstr(term, self.TERM_WINDOW_WIDTH-1)

