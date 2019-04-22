import xml.etree.ElementTree as ET

class File:
    def __init__(self, fname):
        self.fname = fname
        self.root = self._get_file_root(fname)

    def iterate_elements(self):
        return self.root.iter('*')

    def get_element_by_id(self, element_id):
        return self.get_element_by_attribute('id', element_id)

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
    
    @staticmethod
    def _get_file_root(fname):
        return ET.parse(fname).getroot()
