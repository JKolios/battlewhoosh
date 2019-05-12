import os
import os.path

import whoosh.index

from battlescribe_parser.catalogue.file import CatalogueFile
from battlescribe_parser.roster.file import RosterFile
from schema import Schema

CATALOGUE_DATA_DIR = 'input_files/catalogues'
CATALOGUE_INDEX_DIR = 'indices/catalogue_indices'
ROSTER_DATA_DIR = 'input_files/rosters'
ROSTER_INDEX_DIR = 'indices/roster_indices'
PROFILE_TYPES = ['Weapon', 'Model', 'Ability',
                 'Psychic Power', 'Wargear', 'Psyker']


def setup_index(index_dir):
    return whoosh.index.create_in(index_dir, Schema)


def scrape_selections(index):
    selections = []
    for (dirpath, _, file_names) in os.walk(ROSTER_DATA_DIR):
        for file_name in file_names:
            file_path = os.path.join(dirpath, file_name)
            _, ext = os.path.splitext(file_name)
            if ext != '.cat':
                print(f'Ignoring file: {file_path}')
                continue
            print(f'Parsing file: {file_path}')
            cat_file = RosterFile(file_path)
            selections += cat_file.scrape_selections()

    with index.writer() as index_writer:
        for selection in selections:
            index_writer.add_document(**selection)
    return selections


def scrape_profiles(index):
    for profile_type in PROFILE_TYPES:
        print(f'Processing profile type: {profile_type}')
        profiles = scrape_profiles_of_type(profile_type)
        with index.writer() as index_writer:
            for profile in profiles:
                index_writer.add_document(**profile)


def scrape_profiles_of_type(profile_type):
    profiles = []
    for (dirpath, _, file_names) in os.walk(CATALOGUE_DATA_DIR):
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


def main():
    print('Processing catalogues')
    catalogue_index = setup_index(CATALOGUE_INDEX_DIR)
    scrape_profiles(catalogue_index)

    print('Processing rosters')
    roster_index = setup_index(ROSTER_INDEX_DIR)
    scrape_selections(roster_index)

    print('Index creation complete.')


if __name__ == '__main__':
    main()
