import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import FilterDesign as fdes
import pandas as pd
import numpy as np
import scipy.signal as sc
import matplotlib.pyplot as plt

class FilterDesign_controller:
    def __init__(self, appdata_object):
        self.app_data = appdata_object

    def import_data(self, data_path, header, byrow, index):
        try:
            if header:
                imported_data = pd.read_csv(data_path)
            else:
                imported_data = pd.read_csv(data_path, header = None)
        except ValueError as e:
            raise ValueError("Data must be numeric, \n separated be newline.")

        if imported_data.isna().values.any() == True:
            raise ValueError("Data contains Nan values")

        if byrow:
            if imported_data.index.size != 1:
                if index == "-- Select Column --" or index == "-- Select Row --":
                    raise ValueError("Select which Row to import")
                else:
                    index = int(index)

                self.app_data.data = imported_data.iloc[index,:].values
            else:
                self.app_data.data = imported_data.iloc[0,:].values

        else:
            if imported_data.columns.size != 1:
                if index == "-- Select Column --" or index == "-- Select Row --":
                    raise ValueError("Select which Column to import")
                else:
                    index = int(index)

                self.app_data.data = imported_data.iloc[:,index].values
            else:
                self.app_data.data = imported_data.iloc[:,0].values

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

        elif filter_parameters["type"] == "IIR Filter":
            self.app_data.filter = fdes.IIR_filter(P_order = filter_parameters["P_order"],
                                                   P_coefficients = list(filter_parameters["P_coeff"].values()),
                                                   Q_order = filter_parameters["Q_order"],
                                                   Q_coefficients = list(filter_parameters["Q_coeff"].values()))
            self.app_data.filter_type = "IIR Filter"
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
        elif plot_type == "Filter Response":
            if self.app_data.filter_applied:
                if self.app_data.filter_type == "Butterworth":
                    sos = np.zeros([len(self.app_data.filter.IIR_filters), 6])
                    idx = 0
                    for filter in self.app_data.filter.IIR_filters:
                        if filter.P_order == 2:
                            sos[idx] = [filter.P_coeff[0], filter.P_coeff[1], filter.P_coeff[2],
                                        1, filter.Q_coeff[0], filter.Q_coeff[1]]
                            idx += 1
                        elif filter.P_order == 1:
                            sos[idx] = [0, filter.P_coeff[0], filter.P_coeff[1],
                                        1, filter.Q_coeff[0], 0]
                            idx += 1
                    w, h = sc.sosfreqz(sos, worN = None, whole = False)
                    return np.array([w,np.abs(h)])
                if self.app_data.filter_type == "IIR Filter":
                    b = self.app_data.filter.P_coeff
                    a = np.concatenate([[1], self.app_data.filter.Q_coeff])
                    w, h = sc.freqz(b = b, a = a)
                    return np.array([w,np.abs(h)])
            else:
                raise ValueError("Must apply a filter first.")
