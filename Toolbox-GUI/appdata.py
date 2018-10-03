import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import FilterDesign

class FilterDesign_appdata:
    def __init__(self):
        self.data = 0
        self.filtered_data = 0
        self.filter_applied = 0
        self.filter_type = ""
        self.filter = 0
