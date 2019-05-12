import curses

import npyscreen

from search_catalogues.term_text import TermText
from search_catalogues.result_text import ResultText

class SearchForm(npyscreen.FormBaseNew):
    def create(self):
        self.add_handlers({
            "^Q":  self.exit,
            "^W":  self.jump_to_term_text,
            "^E":  self.jump_to_result_text,
            "^R":  self.jump_to_detail_text
        })
        self.term_text = self.add(
            TermText,
            name="Name:",
            height=1,
            scroll_exit=True)
        self.result_text = self.add(
            ResultText,
            name="Results:",
            values=[],
            height=10,
            scroll_exit=True)
        self.detail_text = self.add(
            npyscreen.TitlePager,
            name="Details:",
            scroll_exit=True,
            autowrap=True)
    
    def jump_to_term_text(self, _input):
        self.term_text.edit()
    
    def jump_to_result_text(self, _input):
        self.result_text.edit()
    
    def jump_to_detail_text(self, _input):
        self.detail_text.edit()

    def exit(self, _input):
        quit(0)
