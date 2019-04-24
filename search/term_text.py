import npyscreen
import curses

class TermText(npyscreen.TitleText):

    def when_value_edited(self):
        search_results = self.parent.parentApp.run_search(self.value)
        self.parent.result_text.values = search_results
        self.parent.result_text.display()