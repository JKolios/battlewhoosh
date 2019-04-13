from pprint import pprint
import os
import os.path

from catalogue_file import CatalogueFile
from catalogue_element import CatalogueElement

DATA_DIR = 'datafiles'

def main():
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
            profiles.append(cat_file.scrape_profiles())
    pprint(profiles)

if __name__ == '__main__':
    main()