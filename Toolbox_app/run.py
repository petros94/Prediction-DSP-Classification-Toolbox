from gui import *
from controller import *
from appdata import *

root = tk.Tk()
filter_design_data = FilterDesign_appdata()
filter_design_controller = FilterDesign_controller(filter_design_data)
filter_design_window = FilterDesign_window(root, filter_design_controller)


filter_design_window.mainloop()
