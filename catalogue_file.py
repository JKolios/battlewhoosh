import xml.etree.ElementTree as ET

import ujson

from catalogue_element import CatalogueElement

PROFILE_TYPES = ['Weapon', 'Model', 'Psyker', 'Wargear', 'Ability', 'Psychic Power']

class CatalogueFile:
    def __init__(self, fname):
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

    def scrape_profiles(self):
        profiles = []
        for profile_type in PROFILE_TYPES:
            profiles += (self.scrape_profile_type(profile_type))
        return profiles

    def scrape_profile_type(self, profile_type):
        profiles = self.get_elements_by_attribute('profileTypeName', profile_type)
        profile_json_entries = []
        for profile in profiles:
            profile_json_entries.append(self._scrape_profile(profile))
        return profile_json_entries
            
    def _scrape_profile(self, profile):
        profile_element = CatalogueElement(profile, self)
        profile_data = {}
        for child_element in profile_element.iterate_children():
            child_attributes = child_element.attrib()
            if child_attributes:
                profile_data = {**profile_data, **self._scrape_child_attrs(child_attributes)}
        return profile_data
    
    @staticmethod
    def _get_file_root(fname):
        return ET.parse(fname).getroot()

    @staticmethod
    def _scrape_child_attrs(child_attrs):
        print(child_attrs)
        if 'profileTypeName' in child_attrs.keys():
            return {child_attrs['profileTypeName']: child_attrs['name']}
        if child_attrs.get('type'):
            return {'effect': child_attrs['value']}
        return {child_attrs['name']: child_attrs['value']}