import curses
import pprint


class ResultWindow:

    RESULT_WINDOW_COORDS = [2, 0]
    RESULT_WINDOW_WIDTH = 80

    def __init__(self, max_lines):
        self.window = curses.newwin(
            max_lines,
            self.RESULT_WINDOW_WIDTH,
            self.RESULT_WINDOW_COORDS[0],
            self.RESULT_WINDOW_COORDS[1]
        )
        self.window.immedok(True)

        self.highlighted_line = -1

    def show_results(self, results):
        self.window.erase()
        for line_number, result in enumerate(results):
            self.window.addstr(
                line_number, 0, self.search_result_string(result))
        if len(results) < self.highlighted_line:
            self.highlighted_line = len(results) - 1

    def show_details(self, result):
        self.window.erase()
        self.window.addstr(0, 0, self.detail_string(result))

    def highlight_line(self, line_number):
        self.window.chgat(
            line_number,
            0,
            self.RESULT_WINDOW_WIDTH,
            curses.A_STANDOUT
        )
        self.window.refresh()

    def unhighlight_line(self, line_number):
        self.window.chgat(
            line_number,
            0,
            self.RESULT_WINDOW_WIDTH,
            curses.A_NORMAL
        )
        self.window.refresh()

    @staticmethod
    def search_result_string(hit):
        return f'{hit["name"]} {hit["document_type"]}: {hit["faction"]}'

    @staticmethod
    def detail_string(hit):
        return pprint.pformat(hit)
