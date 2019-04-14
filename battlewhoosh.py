import os
import os.path
import sys

from whoosh import index
from whoosh.index import open_dir
from whoosh.qparser import QueryParser

from catalogue.file import CatalogueFile
from schemas.schema import _Schema
from schemas.model import Model
from schemas.weapon import Weapon

DATA_DIR = 'datafiles'
INDEX_DIR = 'indices'


def discover_schemas():
    return [cls for cls in _Schema.__subclasses__()]


def setup_indices(schema_classes):
    indices = {}
    for schema_class in schema_classes:
        schema_index = index.create_in(INDEX_DIR, schema_class.whoosh_schema)
        indices[schema_class] = schema_index
    return indices


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


def main(argv):
    schemas = discover_schemas()
    indices = setup_indices(schemas)
    for schema_class, idx in indices.items():
        print(f'Processing profile type: {schema_class.profile_type}')
        index_writer = idx.writer()
        profiles = scrape_profiles_of_type(schema_class.profile_type)
        for profile in profiles:
            schema_class.write_document(index_writer, profile)
        index_writer.commit()

    dir_index = open_dir(INDEX_DIR)
    with dir_index.searcher() as searcher:
        weapon_q_parser = QueryParser("name", schema=Weapon.whoosh_schema)
        weapon_q = weapon_q_parser.parse(argv[1])
        weapon_q_results = searcher.search(weapon_q)
        for result in weapon_q_results:
            print(result)

        model_q_parser = QueryParser("name", schema=Model.whoosh_schema)
        model_q = model_q_parser.parse(argv[1])
        model_q_results = searcher.search(model_q)
        for result in model_q_results:
            print(result)


if __name__ == '__main__':
    main(sys.argv)
