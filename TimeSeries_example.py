import TimeSeries as ts
import pandas as pd
import numpy as np
import matplotlib.pyplot

"""Create model instance"""
model = ts.ARIMA_model()


"""Create Timeseries"""
u = pd.read_csv("/Users/Petros/Desktop/shampoo.csv")

for i in range(u.index.size):
    u.loc[i, "value"] = (np.random.uniform() - 0.5)
x = u.copy()
y = u.copy()

"""MA process"""
for i in range(2, u.index.size):
    x.loc[i, "value"] = u.loc[i, "value"] +0.65*u.loc[i-1, "value"] - 0.25*u.loc[i-2, "value"]

"""AR process"""
for i in range(2, u.index.size):
    y.loc[i, "value"] = -0.7*y.loc[i-1, "value"] + 0.2*y.loc[i-2, "value"] + u.loc[i, "value"]


"""Fit ARIMA model"""
model.data = y.iloc[0:990, :]
model.fit_AR_model(p = 2, d =0)
model.summary()

"""Evaluate model"""
model.prediction_error(time_steps = 1, plot_error = 1, plot_residual_autocorr = 1)

"""Predict next two values"""
predictions = model.predict(time_steps = 2)
