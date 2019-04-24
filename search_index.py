import npyscreen

from schema import Schema
from search.application import SearchApp
from search.context import SearchContext

INDEX_DIR = 'catalogue_indices'


def main():
    search_context = SearchContext(INDEX_DIR, Schema.schema())
    SearchApp(search_context).run()


if __name__ == '__main__':
    main()
