from pprint import pprint
import os
import sys
import os.path

from whoosh import fields, index
from whoosh.qparser import QueryParser

from catalogue.file import CatalogueFile
from catalogue.element import CatalogueElement
from schemas.weapon import weapon

DATA_DIR = 'datafiles'
INDEX_DIR = 'indices'

def setup_indices():
    weapon_index = index.create_in(INDEX_DIR, weapon)
    return {
        'weapon': weapon_index
    }

def scrape_all_profiles():
    profiles = []
    for (dirpath, dirnames, file_names) in os.walk(DATA_DIR):
        for file_name in file_names:
            file_path = os.path.join(dirpath, file_name)
            _, ext = os.path.splitext(file_name)
            if ext != '.cat':
                print(f'Ignoring file: {file_path}')
                continue
            print(f'Parsing file: {file_path}')
            cat_file = CatalogueFile(file_path)
            profiles += cat_file.scrape_profiles()
    return profiles

def main(argv):
    indices = setup_indices()
    weapon_index = indices['weapon']
    weapon_writer = weapon_index.writer()
    profiles = scrape_all_profiles()
    for profile in profiles:
        weapon_writer.add_document(
            document_type='weapon',
            faction=profile.get('faction'),
            name=profile.get('name'),
            book=profile.get('book'),
            page=profile.get('page'),
            type=profile.get('Type'),
            range=profile.get('Range'),
            s=profile.get('S'),
            ap=profile.get('AP'),
            d=profile.get('D'),
            abilities=profile.get('Abilities')
        )
    weapon_writer.commit()
    qp = QueryParser("name", schema=weapon_index.schema)
    q = qp.parse(argv[1])

    with weapon_index.searcher() as s:
        results = s.search(q)
        pprint(list(results))
    

if __name__ == '__main__':
    main(sys.argv)
