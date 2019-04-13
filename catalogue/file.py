import xml.etree.ElementTree as ET

import ujson

from catalogue.element import CatalogueElement

PROFILE_TYPES = ['Weapon']

class CatalogueFile:
    def __init__(self, fname):
        self.fname = fname
        self.root = self._get_file_root(fname)
    
    def iterate_elements(self):
        return self.root.iter('*')

    def get_element_by_id(self, id):
        return self.get_element_by_attribute('id', id)
    
    def get_elements_by_type(self, element_type):
        return self.get_elements_by_attribute('type', element_type)
    
    def get_elements_by_name(self, name):
        return self.get_elements_by_attribute('name', name)

    def get_element_by_attribute(self, attribute, value):
        return self.root.find(f".//*[@{attribute}='{value}']")

    def get_elements_by_attribute(self, attribute, value):
        return self.root.findall(f".//*[@{attribute}='{value}']")

    def file_name(self):
        return self.fname

    def scrape_profiles(self):
        profiles = []
        for profile_type in PROFILE_TYPES:
            profiles = [*profiles, *self.scrape_profile_type(profile_type)]
        return profiles

    def scrape_profile_type(self, profile_type):
        profile_elements = self.get_elements_by_attribute('profileTypeName', profile_type)
        profiles = []
        for profile_element in profile_elements:
            profile_element_obj = CatalogueElement(profile_element, self, profile_type)
            profiles.append(profile_element_obj._scrape_profile())
        return profiles
              
    @staticmethod
    def _get_file_root(fname):
        return ET.parse(fname).getroot()
