import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as tkf
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot

class FilterDesign_window(tk.Frame):
    def __init__(self, master, controller = None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.controller = controller
        self.init_window()
        self.next_row = 0
        self.option_graph_2_var_prev = "FFT"
        self.option_graph_1_var_prev = "Original Data"


    def init_window(self):
        self.master.geometry("840x630")
        self.master.title('Prediction-DSP-Classification-Toolbox')

        """Menu"""
        self.label_import_export_title = tk.Label(self.master, text="Import/Export", font=('Helvetica', 14, 'bold'))
        self.label_import_export_title.grid(row = 0, column = 0, columnspan = 2, pady = 5, sticky = "ew")
        self.label_import_data = tk.Label(self.master, text="Import Data: ")
        self.label_import_data.grid(row = 1, column = 0, padx = 5, sticky = "ew")
        self.button_import_data = tk.Button(self.master, text = "Choose Path...", command = self.button_import_data_click)
        self.button_import_data.grid(row = 1, column = 1, padx = 5,  sticky = "ew")
        self.check_import_data_header_var = tk.IntVar()
        self.check_import_data_byrow_var = tk.IntVar()
        self.check_import_data_byrow = tk.Checkbutton(self.master, text = "By Row", variable = self.check_import_data_byrow_var, command = self.check_import_data_byrow_click)
        self.check_import_data_byrow.grid(row = 2, column = 0, padx = 5)
        self.check_import_data_header = tk.Checkbutton(self.master, text = "Header", variable = self.check_import_data_header_var)
        self.check_import_data_header.grid(row = 3, column = 0)
        self.option_import_data_index_var = tk.StringVar(self.master)
        self.option_import_data_index_var.set("-- Select Column --")
        self.option_import_data_index_menu = tk.OptionMenu(self.master, self.option_import_data_index_var, "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10")
        self.option_import_data_index_menu.grid(row = 2, column = 1)

        self.label_export_data = tk.Label(self.master, text="Export Data: ")
        self.label_export_data.grid(row = 4, column = 0, padx = 5, sticky = "ew")
        self.option_export_data_var = tk.StringVar(self.master)
        self.option_export_data_var.set("Filtered Data")
        self.option_export_data_menu = tk.OptionMenu(self.master, self.option_export_data_var, "Filtered Data", "Filter Coefficients", "Filter Response")
        self.option_export_data_menu.grid(row = 4, column = 1, pady = 5, sticky = "ew")
        self.button_export_data = tk.Button(self.master, text = "Export...", command = self.button_export_data_click)
        self.button_export_data.grid(row = 5, column = 0, columnspan =2, padx = 5,  sticky = "ew")
        self.label_import_export_error = tk.Label(self.master)
        self.label_import_export_error.grid(row = 6, column = 0, columnspan = 3, sticky = "ew")

        self.separator_0 = ttk.Separator(self.master, orient="horizontal")
        self.separator_0.grid(row = 7, column = 0, columnspan = 2, sticky = "ew")

        self.label_filter_title = tk.Label(self.master, text="Filter Data", font=('Helvetica', 14, 'bold'))
        self.label_filter_title.grid(row = 8, column = 0, columnspan = 2, pady = 5, sticky = "ew")
        self.label_filter_select = tk.Label(self.master, text="Select Filter:")
        self.label_filter_select.grid(row = 9, column = 0)
        self.option_filter_select_var = tk.StringVar(self.master)
        self.option_filter_select_var.set("Butterworth")
        self.option_filter_select_var.trace(mode = "w", callback = self.update_filter_view)
        self.option_filter_select = tk.OptionMenu(self.master, self.option_filter_select_var, "Butterworth")
        self.option_filter_select.grid(row = 9, column = 1, sticky = "e")

        self.update_filter_view()

        self.separator_1 = ttk.Separator(self.master, orient="horizontal")
        self.separator_1.grid(row = self.next_row, column = 0, columnspan = 2, sticky = "ew")

        self.label_plot_title = tk.Label(self.master, text="Plot", font=('Helvetica', 14, 'bold'))
        self.label_plot_title.grid(row = self.next_row+1, column = 0, columnspan = 2, pady = 5, sticky = "ew")
        self.label_graph_1 = tk.Label(self.master, text = "Graph 1:")
        self.label_graph_1.grid(row = self.next_row+2, column = 0, pady = 5)
        self.option_graph_1_var = tk.StringVar(self.master)
        self.option_graph_1_var.set("Original Data")
        self.option_graph_1_var.trace(mode = "w", callback = self.update_plot_view)
        self.option_graph_1_select = tk.OptionMenu(self.master, self.option_graph_1_var, "Original Data", "FFT", "Filtered Data", "Filter Response")
        self.option_graph_1_select.grid(row = self.next_row + 2, column = 1, pady = 5, sticky = "e")
        self.label_graph_2 = tk.Label(self.master, text = "Graph 2:")
        self.label_graph_2.grid(row = self.next_row+3, column = 0, pady = 5)
        self.option_graph_2_var = tk.StringVar(self.master)
        self.option_graph_2_var.set("FFT")
        self.option_graph_2_var.trace(mode = "w", callback = self.update_plot_view)
        self.option_graph_2_select = tk.OptionMenu(self.master, self.option_graph_2_var, "Original Data", "FFT", "Filtered Data", "Filter Response")
        self.option_graph_2_select.grid(row = self.next_row + 3, column = 1, pady = 5, sticky = "e")

        """Plot"""
        self.figure = matplotlib.pyplot.Figure(figsize=(6,6), dpi=100)
        self.figure_subplot_a = self.figure.add_subplot(211)
        self.figure_subplot_b = self.figure.add_subplot(212)
        self.figure.subplots_adjust(hspace = 0.3)
        self.canvas = FigureCanvasTkAgg(self.figure, self.master)
        self.canvas.get_tk_widget().grid(row = 0, column = 4, rowspan = self.next_row+4, columnspan = 5, sticky = "nwes")

        self.toolbar_frame = tk.Frame(self.master)
        self.toolbar_frame.grid(row = self.next_row+3, column = 4, sticky = "e")
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.toolbar_frame)
        self.toolbar.update()

    """View update functions"""
    def update_filter_view(self, *args):
        if self.option_filter_select_var.get() == "Butterworth":
            self.next_row = 16
            self.label_filter_order = tk.Label(self.master, text="Order:")
            self.label_filter_order.grid(row = 10, column = 0, pady = 5)

            self.option_filter_order_var = tk.IntVar(self.master)
            self.option_filter_order_var.set(1)
            self.option_filter_order = tk.OptionMenu(self.master, self.option_filter_order_var, 1, 2, 3, 4, 5, 6, 7, 8)
            self.option_filter_order.grid(row = 10, column = 1, pady = 5, sticky = "e")

            self.label_filter_cutoff_freq = tk.Label(self.master, text="Analog\n Cutoff\n Frequency (Hz):")
            self.label_filter_cutoff_freq.grid(row = 11, column = 0, pady = 5)
            self.entry_filter_cuttof_freq_var = tk.IntVar(self.master)
            self.entry_filter_cuttof_freq = tk.Entry(self.master, textvariable = self.entry_filter_cuttof_freq_var, justify = "right", width = 12)
            self.entry_filter_cuttof_freq.grid(row = 11, column = 1, pady = 5, sticky = "e")

            self.label_filter_sampling_rate = tk.Label(self.master, text="Sampling Rate\n(Hz):")
            self.label_filter_sampling_rate.grid(row = 12, column = 0, pady = 5)
            self.entry_filter_sampling_rate_var = tk.IntVar(self.master)
            self.entry_filter_sampling_rate = tk.Entry(self.master, textvariable = self.entry_filter_sampling_rate_var, justify = "right", width = 12)
            self.entry_filter_sampling_rate.grid(row = 12, column = 1, pady = 5, sticky = "e")

            self.label_filter_dc_gain = tk.Label(self.master, text="DC Gain (V/V):")
            self.label_filter_dc_gain.grid(row = 13, column = 0, pady = 5)
            self.entry_filter_dc_gain_var = tk.IntVar(self.master)
            self.entry_filter_dc_gain_var.set(1)
            self.entry_filter_dc_gain = tk.Entry(self.master, textvariable = self.entry_filter_dc_gain_var, justify = "right", width = 12)
            self.entry_filter_dc_gain.grid(row = 13, column = 1, pady = 5, sticky = "e")

            self.button_filter_apply = tk.Button(self.master, text = "Apply", command = self.button_filter_apply_click)
            self.button_filter_apply.grid(row = 14, column = 0, columnspan = 2, pady = 5, sticky = "ew")

            self.label_apply_error = tk.Label(self.master)
            self.label_apply_error.grid(row = 15, column = 0, columnspan = 2)


    def update_plot_view(self, *args):
        try:
            graph_1_data = self.controller.get_plot_data(self.option_graph_1_var.get())
            self.option_graph_1_var_prev = self.option_graph_1_var.get()
            self.figure_subplot_a.cla()
            if graph_1_data.shape[0] == 2:
                print("yolo")
                graph_1_data_x = graph_1_data[0]
                graph_1_data_y = graph_1_data[1]
                self.figure_subplot_a.plot(graph_1_data_x, graph_1_data_y, c = "C0")
            else:
                self.figure_subplot_a.plot(graph_1_data, c = "C0")
        except ValueError as e:
            print(e)
            self.option_graph_1_var.set(self.option_graph_1_var_prev)

        try:
            graph_2_data = self.controller.get_plot_data(self.option_graph_2_var.get())
            self.option_graph_2_var_prev = self.option_graph_2_var.get()
            self.figure_subplot_b.cla()
            if graph_2_data.shape[0] == 2:
                graph_2_data_x = graph_2_data[0]
                graph_2_data_y = graph_2_data[1]
                self.figure_subplot_b.plot(graph_2_data_x, graph_2_data_y, c = "C1")
            else:
                self.figure_subplot_b.plot(graph_2_data, c = "C1")
        except ValueError as e:
            print(e)
            self.option_graph_2_var.set(self.option_graph_2_var_prev)

        self.canvas.draw()

    """Button click functions"""
    def button_import_data_click(self):
        data_path = tkf.askopenfilename()
        if not data_path:
            return None
        try:
            self.controller.import_data(data_path, self.check_import_data_header_var.get(),
                                        self.check_import_data_byrow_var.get(),
                                        self.option_import_data_index_var.get())
        except ValueError as e:
            self.label_import_export_error['text'] = e
            self.label_import_export_error['fg'] = "red"
            return None

        self.label_import_export_error['text'] = "Data Imported."
        self.label_import_export_error['fg'] = "green"

        try:
            graph_data = self.controller.get_plot_data("Original Data")
        except ValueError as e:
            print(e)
            return None
        self.update_plot_view()

    def button_export_data_click(self):
        file_name = tkf.asksaveasfilename(filetypes = (("Plain Text", "*.txt"), ("CSV File", "*.csv")))
        if not file_name:
            return None

        try:
            self.controller.export_data(file_name, self.option_export_data_var.get())
        except ValueError as e:
            self.label_import_export_error['text'] = e
            self.label_import_export_error['fg'] = "red"
            return None

        self.label_import_export_error['text'] = "Data Exported."
        self.label_import_export_error['fg'] = "green"

    def button_filter_apply_click(self):
        try:
            filter_parameters = {
                "type": self.option_filter_select_var.get(),
                "order": self.option_filter_order_var.get(),
                "cutoff_freq": self.entry_filter_cuttof_freq_var.get(),
                "sampling_rate": self.entry_filter_sampling_rate_var.get(),
                "dc_gain": self.entry_filter_dc_gain_var.get()
            }
        except tk.TclError as e:
            self.label_apply_error['text'] = "Invalid Parameters."
            self.label_apply_error['fg'] = "red"
            return None

        self.label_apply_error['text'] = ""

        try:
            self.controller.apply_filter(filter_parameters)
        except ValueError as e:
            print(e)
            return None

        self.update_plot_view()
        print("Filter Applied.")

    def check_import_data_byrow_click(self):
        if self.check_import_data_byrow_var.get():
            self.option_import_data_index_var.set("-- Select Row --")
        else:
            self.option_import_data_index_var.set("-- Select Column --")
