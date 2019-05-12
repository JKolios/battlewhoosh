from schema import Schema
from search_ui.catalogues.application import SearchApp
from search_context.context import SearchContext

INDEX_DIR = 'indices/catalogue_indices'


def main():
    search_context = SearchContext(INDEX_DIR, Schema.schema())
    SearchApp(search_context).run()


if __name__ == '__main__':
    main()
