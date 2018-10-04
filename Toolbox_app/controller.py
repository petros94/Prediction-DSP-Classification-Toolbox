import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import FilterDesign as fdes
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class FilterDesign_controller:
    def __init__(self, appdata_object):
        self.app_data = appdata_object

    def import_data(self, data_path):
        try:
            imported_data = np.loadtxt(data_path)
        except ValueError as e:
            raise ValueError("Data must be one-dimensional numeric, \n separated be newline.")

        if len(imported_data.shape) != 1:
            raise ValueError("Data must be one-dimensional numeric, \n separated by newline.")

        self.app_data.data = np.loadtxt(data_path)

    def export_data(self, data_path, data_type):
        if not self.app_data.filter_applied:
            raise ValueError("Must apply a filter first.")

        if data_type == "Filtered Data":
            np.savetxt(data_path, self.app_data.filtered_data)

        elif data_type == "Filter Coefficients":
            if self.app_data.filter_type == "Butterworth":
                colnames = []
                d = dict()
                index = 0
                for filter in self.app_data.filter.IIR_filters:
                    colnames.append("IIR_Filter_" + str(index) + "_P_coeff")
                    colnames.append("IIR_Filter_" + str(index) + "_Q_coeff")
                    index += 1

                dataframe = pd.DataFrame(index = range(3), columns = colnames)

                """Format dataframe properly"""
                for j in range(len(self.app_data.filter.IIR_filters)):
                    for i in range(len(self.app_data.filter.IIR_filters[j].P_coeff)):
                        dataframe.iloc[i, 2*j] = self.app_data.filter.IIR_filters[j].P_coeff[i]
                    for i in range(len(self.app_data.filter.IIR_filters[j].Q_coeff)):
                        dataframe.iloc[i, 2*j+1] = self.app_data.filter.IIR_filters[j].Q_coeff[i]
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

    def get_plot_data(self, plot_type):
        if plot_type == "Original Data":
            if type(self.app_data.data) == np.ndarray:
                return self.app_data.data
            else:
                raise ValueError("Error: Must import data first.")

        elif plot_type == "Filtered Data":
            if self.app_data.filter_applied:
                return self.app_data.filtered_data
            else:
                raise ValueError("Must apply a filter first.")
        elif plot_type == "FFT":
            if type(self.app_data.data) == np.ndarray:
                return np.abs(np.fft.fft(self.app_data.data))
            else:
                raise ValueError("Error: Must import data first.")
