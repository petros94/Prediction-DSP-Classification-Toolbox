import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import FilterDesign
import pandas as pd
import numpy as np

class FilterDesign_controller:
    def __init__(self, appdata_object):
        self.appdata_object = appdata_object
        pass

    def get_data(self):
        pass

    def import_data(self, data_path):
        try:
            imported_data = pd.read_csv(data_path, dtype = np.float)
        except ValueError as e:
            raise ValueError("Data must be one-dimensional numeric, \n separated by commas.")

        if imported_data.columns.size != 1:
            raise ValueError("Data must be one-dimensional numeric, \n separated by commas.")

        self.appdata_object.data = imported_data.values

    def export_data(self, data_path, data_type):
        if not self.appdata_object.filter_applied:
            raise ValueError("Must apply a filter first.")

        if data_type == "Filtered Data":
            np.savetxt(data_path, self.appdata_object.filtered_data)

        elif data_type == "Filter Coefficients":
            if self.appdata_object.filter_type == "Butterworth":
                dataframe = pd.DataFrame({"P_coeff": self.appdata_object.filter.P_coeff,
                                          "Q_coeff": self.appdata_object.filter.Q_coeff})
                dataframe.to_csv(data_path)
        pass
