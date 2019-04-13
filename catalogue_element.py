from xml.etree.ElementTree import Element

INTERNAL_ATTRS = {'id','characteristicTypeId', 'hidden', 'TypeId', 'profileTypeId'}

class CatalogueElement:

    def __init__(self, xml_element, catalogue_file):
        self.element = xml_element
        self.catalogue_file = catalogue_file
    
    def attrib(self):
        returned_keys = set(self.element.attrib.keys()) - INTERNAL_ATTRS
        return {k: v for k,v in self.element.attrib.items() if k in returned_keys}

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

    def _resolve_associated_element(self, element_id):
        associated_element = self.catalogue_file.get_element_by_id(element_id)
        return CatalogueElement(associated_element, self.catalogue_file)