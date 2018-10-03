import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as tkf

class FilterDesign_window(tk.Frame):
    def __init__(self, master, controller = None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.controller = controller
        self.init_window()


    def init_window(self):
        self.master.geometry("800x600")
        self.master.title('Prediction-DSP-Classification-Toolbox')

        self.label_import_export_title = tk.Label(self.master, text="Import/Export Data", font=('Helvetica', 14, 'bold'))
        self.label_import_export_title.grid(row = 0, column = 0, columnspan = 2, pady = 5, sticky = "ew")
        self.label_import_data = tk.Label(self.master, text="Import Data: ")
        self.label_import_data.grid(row = 1, column = 0, padx = 5, sticky = "ew")
        self.button_import_data = tk.Button(self.master, text = "Choose Path...", command = self.button_import_data_click)
        self.button_import_data.grid(row = 1, column = 1, padx = 5,  sticky = "ew")
        self.label_import_error = tk.Label(self.master)
        self.label_import_error.grid(row = 2, column = 0, columnspan = 3, sticky = "ew")

        self.label_export_data = tk.Label(self.master, text="Export Data: ")
        self.label_export_data.grid(row = 3, column = 0, padx = 5, sticky = "ew")
        self.option_export_data_var = tk.StringVar(self.master)
        self.option_export_data_var.set("Filtered Data")
        self.option_export_data_menu = tk.OptionMenu(self.master, self.option_export_data_var, "Filtered Data", "Filter Coefficients", "Filter Response")
        self.option_export_data_menu.grid(row = 3, column = 1, sticky = "ew")
        self.button_export_data = tk.Button(self.master, text = "Export...", command = self.button_export_data_click)
        self.button_export_data.grid(row = 4, column = 0, columnspan =2, padx = 5,  sticky = "ew")
        self.label_export_error = tk.Label(self.master)
        self.label_export_error.grid(row = 5, column = 0, columnspan = 3, sticky = "ew")

        self.separator_0 = ttk.Separator(self.master, orient="horizontal")
        self.separator_0.grid(row = 6, column = 0, columnspan = 2, sticky = "ew")

        self.label_filter_title = tk.Label(self.master, text="Filter Data", font=('Helvetica', 14, 'bold'))
        self.label_filter_title.grid(row = 7, column = 0, columnspan = 2, pady = 5, sticky = "ew")
        self.label_filter_select = tk.Label(self.master, text="Select Filter:")
        self.label_filter_select.grid(row = 8, column = 0)
        self.option_filter_select_var = tk.StringVar(self.master)
        self.option_filter_select_var.set("Butterworth")
        self.option_filter_select_var.trace(mode = "w", callback = self.update_filter_view)
        self.option_filter_select = tk.OptionMenu(self.master, self.option_filter_select_var, "Butterworth")
        self.option_filter_select.grid(row = 8, column = 1, sticky = "e")

        self.update_filter_view()

    def update_filter_view(self, *args):
        if self.option_filter_select_var.get() == "Butterworth":
            self.label_filter_order = tk.Label(self.master, text="Order:")
            self.label_filter_order.grid(row = 9, column = 0, pady = 5)

            self.option_filter_order_var = tk.IntVar(self.master)
            self.option_filter_order_var.set(1)
            self.option_filter_order = tk.OptionMenu(self.master, self.option_filter_order_var, 1, 2, 3, 4, 5, 6, 7, 8)
            self.option_filter_order.grid(row = 9, column = 1, pady = 5, sticky = "e")

            self.label_filter_cutoff_freq = tk.Label(self.master, text="Analog\n Cutoff\n Frequency (Hz):")
            self.label_filter_cutoff_freq.grid(row = 10, column = 0, pady = 5)
            self.entry_filter_cuttof_freq_var = tk.IntVar(self.master)
            self.entry_filter_cuttof_freq = tk.Entry(self.master, textvariable = self.entry_filter_cuttof_freq_var, justify = "right", width = 12)
            self.entry_filter_cuttof_freq.grid(row = 10, column = 1, pady = 5, sticky = "e")

            self.label_filter_sampling_rate = tk.Label(self.master, text="Sampling Rate\n(Hz):")
            self.label_filter_sampling_rate.grid(row = 11, column = 0, pady = 5)
            self.entry_filter_sampling_rate_var = tk.IntVar(self.master)
            self.entry_filter_sampling_rate = tk.Entry(self.master, textvariable = self.entry_filter_sampling_rate_var, justify = "right", width = 12)
            self.entry_filter_sampling_rate.grid(row = 11, column = 1, pady = 5, sticky = "e")

            self.button_filter_apply = tk.Button(self.master, text = "Apply", command = self.button_filter_apply_click)
            self.button_filter_apply.grid(row = 12, column = 0, columnspan = 2, pady = 5, sticky = "ew")

    """Button click functions"""
    def button_import_data_click(self):
        data_path = tkf.askopenfilename()
        if not data_path:
            return None

        try:
            self.controller.import_data(data_path)
        except ValueError as e:
            self.label_import_error['text'] = e
            self.label_import_error['fg'] = "red"
            return None

        self.label_import_error['text'] = "Data Imported"
        self.label_import_error['fg'] = "green"

    def button_export_data_click(self):
        file_name = tkf.asksaveasfilename(filetypes = (("Plain Text", "*.txt"), ("CSV File", "*.csv")))
        if not file_name:
            return None

        try:
            self.controller.export_data(file_name, self.option_export_data_var)
        except ValueError as e:
            self.label_export_error['text'] = e
            self.label_export_error['fg'] = "red"
            return None

        self.label_export_error['text'] = "Data Exported"
        self.label_export_error['fg'] = "green"

    def button_filter_apply_click(self):
        pass
