import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import FilterDesign as fdes
import pandas as pd
import numpy as np

class FilterDesign_controller:
    def __init__(self, appdata_object):
        self.app_data = appdata_object
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

        self.app_data.data = imported_data.values

    def export_data(self, data_path, data_type):
        if not self.app_data.filter_applied:
            raise ValueError("Must apply a filter first.")

        if data_type == "Filtered Data":
            np.savetxt(data_path, self.app_data.filtered_data)

        elif data_type == "Filter Coefficients":
            if self.app_data.filter_type == "Butterworth":
                dataframe = pd.DataFrame({"P_coeff": self.app_data.filter.P_coeff,
                                          "Q_coeff": self.app_data.filter.Q_coeff})
                dataframe.to_csv(data_path)
        pass

    def apply_filter(self, filter_parameters):
        if type(self.app_data.data) != np.ndarray:
            raise ValueError("Error: Must import data first.")

        if filter_parameters["type"] == "Butterworth":
            if filter_parameters["sampling_rate"] <= 0 or filter_parameters["cutoff_freq"] <= 0:
                raise ValueError("Error: Sampling rate and Cutoff Frequency must be positive.")

            self.app_data.filter = fdes.Butterworth_filter(sampling_period = 1/filter_parameters["sampling_rate"],
                                               filter_order = filter_parameters["order"],
                                               analog_cutoff_freq = filter_parameters["cutoff_freq"],
                                               DC_Gain = filter_parameters["dc_gain"])
            self.app_data.filter_type = "Butterworth"

            self.app_data.filtered_data = self.app_data.filter.apply(self.app_data.data)
            self.app_data.filter_applied = True
