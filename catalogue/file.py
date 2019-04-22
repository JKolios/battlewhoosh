import bsdata.file
from catalogue.element import CatalogueElement


class CatalogueFile(bsdata.file.File):

    def scrape_profile_type(self, profile_type):
        profile_elements = self.get_elements_by_attribute(
            'profileTypeName', profile_type)
        profiles = []
        for profile_element in profile_elements:
            catalogue_element = CatalogueElement(
                profile_element, self, profile_type)
            profiles.append(catalogue_element.scrape_profile())
        return profiles
