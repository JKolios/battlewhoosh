import os
import os.path

import whoosh
from whoosh.qparser import QueryParser

from catalogue.file import CatalogueFile
from schema import Schema

DATA_DIR = 'datafiles'
INDEX_DIR = 'indices'
PROFILE_TYPES = ['Weapon', 'Model', 'Ability',
                 'Psychic Power', 'Wargear', 'Astra Militarum Orders',
                 'unit']


def setup_index():
    return whoosh.index.create_in(INDEX_DIR, Schema)


def scrape_profiles_of_type(profile_type):
    profiles = []
    for (dirpath, _, file_names) in os.walk(DATA_DIR):
        for file_name in file_names:
            file_path = os.path.join(dirpath, file_name)
            _, ext = os.path.splitext(file_name)
            if ext != '.cat':
                print(f'Ignoring file: {file_path}')
                continue
            print(f'Parsing file: {file_path}')
            cat_file = CatalogueFile(file_path)
            profiles += cat_file.scrape_profile_type(profile_type)
    return profiles


def search(index, default_attribute, query_string, max_results=None):
    with index.searcher() as searcher:
        query_parser = QueryParser(default_attribute, schema=Schema.schema())
        query = query_parser.parse(query_string)
        search_hits = searcher.search(query, limit=max_results)
        return [hit.fields() for hit in search_hits]


def main():
    index = setup_index()
    for profile_type in PROFILE_TYPES:
        print(f'Processing profile type: {profile_type}')
        profiles = scrape_profiles_of_type(profile_type)
        with index.writer() as index_writer:
            for profile in profiles:
                index_writer.add_document(**profile)
    print('Index creation complete.')


if __name__ == '__main__':
    main()
