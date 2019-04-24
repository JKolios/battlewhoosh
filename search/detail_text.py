import curses

import npyscreen

class DetailText(npyscreen.MultiLine):
    
    def display_value(self, vl):
        return f'{vl["name"]} {vl["document_type"]}: {vl["faction"]}'

