import sys
try:
    import numpy
    import pandas
    import matplotlib
except ImportError as e:
    print("Missing python packages: please install Numpy, SciPy, Pandas and Matplotlib")
    sys.exit()

print("Requirements met.")
sys.exit()
