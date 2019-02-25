# Prediction-DSP-Classification-Toolbox
A collection of the most popular prediction techniques, implemented in python

This project is a collection of DSP, timeseries analysis and machine learning packages, presented
in a single toolbox with an easy to use GUI.

So far we've implemented some filter design techniques and the corresponding interface.
We ultimately aim to cover most of the algorithms used in ML today. The package up to this
point includes:

### Filter Design Application ###

The Filter Design Application is an easy to use GUI tool, for signal analysis and filtering. It can be used for spectal
analysis of the given data, and filter designing.
The Filter Design Toolbox offers:

* __Import/Export Data__: Import your data from .txt or .csv file formats. You can import specific rows, or columns.
Export multiple things like filter parameters, plots, data after processing, etc.

* __Apply popular filters__: Apply Butterworth, IIR, FIR filters with the desired frequency response and sampling rate.

* __Plot data__: Plot your data before and after filtering, as well as, the DFT and frequency response of the filter.

### Screenshots ###
![Alt text](Screenshots/window1.png?raw=true "Application Window")


### How to run the application ###

First use terminal to download the repository with:

_git clone https://github.com/petros94/Prediction-DSP-Classification-Toolbox_

Then from the top level directory do:

_cd Toolbox_app/; python3 check_dependancies.py_

This script is used to check if you have all the required python packages installed. This toolbox uses:Python3, Numpy, Scipy,
Pandas and Matplotlib. Install any required package using:

_pip3 install package_name_

After installing the necessary packages run the following:

_python3 run.py_
