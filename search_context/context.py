import whoosh
import whoosh.qparser


class SearchContext:
    def __init__(self, index_dir, schema):
        self.schema = schema
        self.index = self._get_index(index_dir, schema)

    def search(self, default_attributes, query_string, max_results=None):
        with self.index.searcher() as searcher:
            query_parser = whoosh.qparser.MultifieldParser(
                default_attributes, self.schema)
            query = query_parser.parse(query_string)
            search_hits = searcher.search(query, limit=max_results)
            return [hit.fields() for hit in search_hits]

    def _get_index(self, directory, schema):
        return whoosh.index.open_dir(directory, readonly=True, schema=schema)
