from statsmodels.tsa.arima_model import *
from statsmodels.tsa.statespace.sarimax import *
import matplotlib.pyplot
import pandas as pd
import numpy as np

"""Utilities"""
def autocorr(data, max_lag, plot = 0):
    autocov = np.zeros(max_lag)
    if type(data) == np.ndarray:
        n = len(data)
        m = np.mean(data)

        if max_lag >= n:
            raise ValueError("max lag must be less than the length of the time series")

        for t in range(max_lag):
            sum = 0
            for i in range(t, n):
                sum += (data[i]-m)*(data[i-t]-m)

            autocov[t] = sum/(n-t)
    else:
        n = data.index.size
        m = np.mean(data.loc[:,"value"])

        if max_lag >= n:
            raise ValueError("max lag must be less than the length of the time series")

        for t in range(max_lag):
            sum = 0
            for i in range(t, n):
                sum += (data.loc[i,"value"]-m)*(data.loc[i-t, "value"]-m)

            autocov[t] = sum/(n-t)

    autocorrelation = autocov/autocov[0]

    if plot != 0:
        matplotlib.pyplot.figure(3)
        matplotlib.pyplot.title("Autocorrelation plot")
        matplotlib.pyplot.plot(np.array(range(0,max_lag)), autocorrelation)
        margin = 1.96/np.sqrt(max_lag)
        matplotlib.pyplot.axhline(y=margin, color='r', linestyle='--')
        matplotlib.pyplot.axhline(y=-margin, color='r', linestyle='--')
        matplotlib.pyplot.show()

    return autocorrelation

def random_check(data, max_lag):
    r = autocorr(data, max_lag, 0)
    margin = 1.96/np.sqrt(max_lag)
    if np.sum(np.abs(r)>margin) - 1 <= 0.05*max_lag:
        return True
    else:
        return False

def lag_operator(data):
    n = data.index.size - 1
    diff = np.array(data.loc[1:n, "value"]) - np.array(data.loc[0:(n-1), "value"])
    lag_data = pd.DataFrame({"time": np.array(data.loc[1:, "time"]), "value": diff})
    return lag_data



"""Linear ARIMA model"""

class ARIMA_model:
    def __init__(self):
        """model parameters"""
        self.model = 0
        self.model_d_param = 0
        self.model_type = 0
        self.model_p_params = 0
        self.model_q_params = 0
        self.model_order = 0

        """prediction errors"""
        self.one_step_prediction_mse = 0
        self.one_step_prediction_rmse = 0
        self.one_step_prediction_nmse = 0

        self.data = 0
        self.diff_data = 0
        self.autocorr_data = 0

    def import_data(self, data_path, nrows = 0):

        if nrows == 0:
            self.data = pd.read_csv(data_path)
        else:
            self.data = pd.read_csv(data_path).iloc[0:nrows, :]

        if self.data.columns.size != 2:
            raise ValueError("Data must have exactly 2 columns - time and value")

        old_names = self.data.columns
        self.data = self.data.rename(columns = {old_names[0]: "time", old_names[1]: "value"})

    def predict(self, start = None, time_steps = 1, plot = 0):
        pred = np.zeros(time_steps)
        if start == None:
            start = self.data.index.size
        elif start > self.data.index.size:
            raise ValueError("start must be equal or less than the data size")
        if self.model_type == "MA":
            prev_z = np.zeros(start)

            for i in range(self.model_order, start):
                prev_z[i] = self.data.loc[i, "value"]
                for k in range(len(self.model_q_params)):
                    prev_z[i] -= self.model_q_params[k]*prev_z[i-1-k]

            for k in range(time_steps):
                for j in range(k, self.model_order):
                    pred[k] += self.model_q_params[j]*prev_z[start-1 - (j-k)]

        elif self.model_type == "AR":
            window = self.data.iloc[(start - self.model_order) : start, 1].values.copy()
            for k in range(time_steps):
                for i in range(self.model_order):
                    pred[k] += self.model_p_params[i]*window[self.model_order - 1 - i]


                for j in range(len(window)-1):
                    window[j] = window[j+1]

                window[self.model_order - 1] = pred[k]
        return pred

    """Model evaluation functions"""

    def prediction_error(self, time_steps, plot_error = 0, plot_residual_autocorr = 0):
        predicted_values = np.zeros(self.data.index.size - time_steps - self.model_order)
        actual_values =  np.zeros(self.data.index.size - time_steps - self.model_order)
        error =  np.zeros(self.data.index.size - time_steps - self.model_order)

        """Calculate prediction error"""
        for i in range(self.model_order, self.data.index.size-time_steps):
            pred = self.predict(start = i+1, time_steps = time_steps)
            predicted_values[i - self.model_order] = pred[time_steps-1]
            actual_values[i - self.model_order] = self.data.loc[i + time_steps, "value"]
            error[i - self.model_order] = self.data.loc[i + time_steps, "value"] - pred[time_steps-1]

        """Calculate root mean square error"""
        mse = np.sum(error**2)/len(error)
        rmse = np.sqrt(mse)

        x_mean = np.mean(actual_values)
        std = np.sqrt(np.sum((actual_values - x_mean)**2)/len(actual_values))
        nmse = rmse / std

        """Plot last 100 values"""
        if plot_error != 0:
            min_ = len(error) - min(100, len(error))
            max_ = len(error)
            matplotlib.pyplot.figure(4)
            matplotlib.pyplot.title("Predicted and Actual Values")
            matplotlib.pyplot.plot(predicted_values[min_ : max_ ], label = "error")
            matplotlib.pyplot.plot(actual_values[min_ : max_ ], label = "error")
            matplotlib.pyplot.axhline(y=rmse, color='r', linestyle='--', label = "rmse")
            matplotlib.pyplot.axhline(y=nmse, color='y', linestyle='--', label = "rmse")

        """plot residuals autocorrelation to check if residuals is white noise"""
        if plot_residual_autocorr != 0:
            autocorr(error, 50, 1)

        return mse, rmse, nmse

    def summary(self):
        print("Model Type:", self.model_type)
        print("Model Order:", self.model_order)
        print("Model p parameters:", self.model_p_params)
        print("Model q parameters:", self.model_q_params)
        print("One-step prediction mse:", self.one_step_prediction_mse)
        print("One-step prediction rmse:", self.one_step_prediction_rmse)
        print("One-step prediction nmse:", self.one_step_prediction_nmse)


    def first_difference(self):
        n = self.data.index.size - 1
        diff = np.array(self.data.loc[1:n, "value"]) - np.array(self.data.loc[0:(n-1), "value"])
        self.diff_data = pd.DataFrame({"time": np.array(self.data.loc[1:, "time"]), "value": diff})
        return self.diff_data

    def n_difference(self, d):
        self.diff_data = self.data
        diff = np.array(self.diff_data.loc[:,"value"])
        n = len(diff)
        for i in range(d):
            diff = diff[1:n] - diff[0:(n-1)]
            n -= 1
        self.diff_data = pd.DataFrame({"time": np.array(self.data.loc[d:, "time"]), "value": diff})
        return self.diff_data

    def fit_AR_model(self, p, d):
        ar = ARIMA(self.data.loc[:,"value"], order = (p, d, 0))
        self.model = ar.fit(disp = 0)
        self.model_order = p
        self.model_p_params = self.model.arparams
        self.model_d_param = d
        self.model_type = "AR"
        mse, rmse, nmse = self.prediction_error(time_steps = 1, plot_error = 0, plot_residual_autocorr = 0)
        self.one_step_prediction_mse, self.one_step_prediction_rmse, self.one_step_prediction_nmse = mse, rmse, nmse

    def fit_MA_model(self, q, d):
        ma = ARIMA(self.data.loc[:,"value"], order = (0, d, q))
        self.model = ma.fit(disp = 0, method = "css")
        self.model_order = q
        self.model_q_params = self.model.maparams
        self.model_d_param = d
        self.model_type = "MA"
