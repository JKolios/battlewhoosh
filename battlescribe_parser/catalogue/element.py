import battlescribe_parser.bsdata.element

class CatalogueElement(battlescribe_parser.bsdata.element.Element):
    def __init__(self, xml_element, catalogue_file, profile_type):
        super().__init__(xml_element, catalogue_file)
        self.profile_type = profile_type

    def scrape_profile(self):
        profile_data = {
            'game': self.game(),
            'faction': self.faction(),
            'document_type': self.profile_type
        }
        for child_element in self.iterate_children():
            child_attributes = child_element.attrib()
            if child_attributes:
                profile_data = {**profile_data, **
                                self._scrape_attrs(child_attributes)}
        return profile_data

    def _scrape_attrs(self, attrs):
        # FIXME: This is hacky and must be refactored
        try:
            if self._is_profile(attrs):
                return {
                    'document_type': attrs.get('profileTypeName'),
                    'name': attrs['name'],
                    'book': attrs.get('book'),
                    'page': attrs.get('page')
                }
            if self._is_value(attrs):
                if attrs['name'] == 'Psychic Power':
                    return {'PsychicPower': attrs['value']}
                if attrs['name'] == 'Warp Charge':
                    return {'WarpCharge': attrs['value']}
                if attrs['name'] == 'Powers known':
                    return {'PowersKnown': attrs['value']}
                return {attrs['name']: attrs['value']}
            return {}
        except KeyError as exception:
            print(f'Exception: {exception} Attributes: {attrs} Profile Type: {self.profile_type}')
            return {}

    @staticmethod
    def _is_value(attributes):
        return 'value' in attributes.keys()

    @staticmethod
    def _is_profile(attributes):
        return 'profileTypeName' in attributes.keys()
