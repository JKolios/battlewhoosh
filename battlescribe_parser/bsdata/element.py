import os.path

class Element:
    INTERNAL_ATTRS = {'id', 'characteristicTypeId', 'hidden', 'TypeId', 'profileTypeId'}

    DIR_TO_GAME_MAPPING = {
        'wh40k-killteam': 'Warhammer 40K: Kill Team',
    }

    def __init__(self, xml_element, catalogue_file, profile_type=None):
        self.element = xml_element
        self.catalogue_file = catalogue_file
        self.profile_type = profile_type

    def attrib(self):
        returned_keys = set(self.element.attrib.keys()) - self.INTERNAL_ATTRS
        return {k: v for k, v in self.element.attrib.items() if k in returned_keys}

    def iterate_children(self):
        children_iterator = self.element.iter('*')
        return (Element(child, self.catalogue_file) for child in children_iterator)

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

    def faction(self):
        file_name = os.path.split(self.catalogue_file.file_name())[1]
        return os.path.splitext(file_name)[0]

    def game(self):
        _, game_dir = os.path.split(os.path.dirname(self.catalogue_file.file_name()))
        return self.DIR_TO_GAME_MAPPING[game_dir]

    def _resolve_associated_element(self, element_id):
        associated_element = self.catalogue_file.get_element_by_id(element_id)
        return Element(associated_element, self.catalogue_file)
    