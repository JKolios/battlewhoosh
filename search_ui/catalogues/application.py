import npyscreen

from search_ui.catalogues.form import SearchForm

MAX_RESULT_LINES = 40

class SearchApp(npyscreen.NPSAppManaged):
    def __init__(self, search_context):
        super().__init__()
        self.search_context = search_context

    def onStart(self):
        self.registerForm("MAIN", SearchForm())

    def run_search(self, term):
        return self.search_context.search(
            ['name', 'document_type'],
            term,
            max_results=MAX_RESULT_LINES)
