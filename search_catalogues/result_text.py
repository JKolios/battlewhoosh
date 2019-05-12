import npyscreen

class ResultText(npyscreen.MultiLine):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value_changed_callback = self.show_details

    def display_value(self, vl):
        return f'{vl["name"]} {vl["document_type"]}: {vl["faction"]}'


    def show_details(self, widget=None):
        if self.value is not None:
            search_result = self.values[self.value]
            self.parent.detail_text.values = [f'{key}:{val}' for key, val in search_result.items()]
            self.parent.detail_text.edit()
            self.parent.detail_text.clear()
            self.parent.detail_text.display()
