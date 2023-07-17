import tkinter as tk


class dataFrame(tk.Frame):
    def __init__(self, parent, data):
        super().__init__(parent, padx=10, pady=10,
                         relief=tk.RIDGE, borderwidth=5, highlightthickness=2)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=4)
        self.data = data
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=4)
        self.rowconfigure(tuple(range(0, 18)), weight=1)
        self.grid(sticky="nsew")

        self.title_label = tk.Label(self, text=f"Data Values")
        self.title_label.grid(row=0, column=0, columnspan=5, sticky="ew")

        self.checkbox_value_16 = []
        self.checkbox_value_32 = []

        self.data_value_16 = ["0"]*16
        self.data_value_32 = ["0"]*16

        # List to store data_label widgets
        self.data_labels = [[None] * 2 for _ in range(16)]

        for _ in range(0, 16):
            self.checkbox_value_16.append(tk.BooleanVar(value=False))
            self.checkbox_value_32.append(tk.BooleanVar(value=False))

        for row in range(1, 17):
            # Create checkbox in column 0
            self.checkbox = tk.Checkbutton(self, variable=self.checkbox_value_16[row-1])
            self.checkbox.grid(row=row, column=0, sticky="nsew")

            # Create data label in column 1
            self.data_labels[row-1][0] = tk.Label(self, text=self.data_value_16[row-1])
            self.data_labels[row-1][0].grid(row=row, column=1, sticky="nsew")

            # Create checkbox in column 3
            self.checkbox = tk.Checkbutton(self, variable=self.checkbox_value_32[row-1])
            self.checkbox.grid(row=row, column=3, sticky="nsew")

            # Create data label in column 4
            self.data_labels[row-1][1] = tk.Label(self, text=self.data_value_32[row-1])
            self.data_labels[row-1][1].grid(row=row, column=4, sticky="nsew")
