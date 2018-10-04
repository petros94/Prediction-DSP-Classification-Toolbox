import sys
try:
    import numpy
    import pandas
    import matplotlib
except ImportError as e:
    print("Requirements not met, please install Numpy, Pandas and Matplotlib")
    sys.exit()

print("Requirements met.")
sys.exit()
