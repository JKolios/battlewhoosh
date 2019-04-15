import os.path

INTERNAL_ATTRS = {'id', 'characteristicTypeId',
                  'hidden', 'TypeId', 'profileTypeId'}
DIR_TO_GAME_MAPPING = {
    'datafiles/wh40k': 'Warhammer 40K',
    'datafiles/wh40k-killteam': 'Warhammer 40K: Kill Team',
}


class CatalogueElement:

    def __init__(self, xml_element, catalogue_file, profile_type=None):
        self.element = xml_element
        self.catalogue_file = catalogue_file
        self.profile_type = profile_type

    def attrib(self):
        returned_keys = set(self.element.attrib.keys()) - INTERNAL_ATTRS
        return {k: v for k, v in self.element.attrib.items() if k in returned_keys}

    def iterate_children(self):
        children_iterator = self.element.iter('*')
        return (CatalogueElement(child, self.catalogue_file) for child in children_iterator)

    def has_child(self):
        return self.child() is not None

    def has_link(self):
        return self.link_target() is not None

    def link_target(self):
        return self.element.get('targetId')

    def child(self):
        return self.element.get('childId')

    def resolve_link(self):
        if not self.has_link():
            return None
        return self._resolve_associated_element(self.link_target())

    def resolve_child(self):
        if not self.has_child():
            return None
        return self._resolve_associated_element(self.child())

    def game(self):
        directory = os.path.dirname(self.catalogue_file.file_name())
        return DIR_TO_GAME_MAPPING[directory]

    def faction(self):
        file_name = os.path.split(self.catalogue_file.file_name())[1]
        return os.path.splitext(file_name)[0]

    def _resolve_associated_element(self, element_id):
        associated_element = self.catalogue_file.get_element_by_id(element_id)
        return CatalogueElement(associated_element, self.catalogue_file)

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
                                self._scrape_child_attrs(child_attributes)}
        return profile_data

    def _scrape_child_attrs(self, child_attrs):
        # FIXME: This is hacky and must be refactored
        try:
            if 'value' in child_attrs.keys():
                if child_attrs['name'] == 'Psychic Power':
                    return {'PsychicPower': child_attrs['value']}
                if child_attrs['name'] == 'Warp Charge':
                    return {'WarpCharge': child_attrs['value']}
                return {child_attrs['name']: child_attrs['value']}
            if 'profileTypeName' in child_attrs.keys():
                return {
                    'document_type': child_attrs.get('profileTypeName'),
                    'name': child_attrs['name'],
                    'book': child_attrs.get('book'),
                    'page': child_attrs.get('page')
                }
            return {}
        except KeyError as exception:
            print(f'Exception: {exception}')
            return {}
