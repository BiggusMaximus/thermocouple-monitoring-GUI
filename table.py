import threading
import tkinter as tk
from tkinter import ttk
from tkinter import ttk, filedialog
import os, csv
import pandas as pd


class tableFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padx=10, pady=10,
                         relief=tk.RIDGE, borderwidth=5, highlightthickness=2)
        self.columnconfigure(0, weight=19)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=8)
        self.rowconfigure(1, weight=2)
        self.rowconfigure(2, weight=1)
        self.tree = ttk.Treeview(self, show="headings")
        self.tree["columns"] = tuple(range(33))
        self.count = 0

        self.tree.heading(0, text="Time")
        for col in range(1, 33):
            self.tree.heading(col, text=f"Data {col}")
            self.tree.column(col, anchor="center")

        self.y_scrollbar = tk.Scrollbar(
            self,
            orient=tk.VERTICAL,
            command=self.tree.yview,
            activebackground='#00ff00'
        )
        self.x_scrollbar = tk.Scrollbar(
            self,
            orient=tk.HORIZONTAL,
            command=self.tree.xview,
            activebackground='#00ff00'
        )

        self.tree.configure(yscroll=self.y_scrollbar.set)
        self.tree.configure(xscroll=self.x_scrollbar.set)
        self.tree.grid(row=0,  column=0, sticky="nsew")
        self.y_scrollbar.grid(row=0, column=1, sticky="nse")
        self.x_scrollbar.grid(row=1, column=0, sticky="sew")

        self.saveExcelButton = tk.Button(
            self, text="Save To Excel",
            relief="groove",
            highlightbackground="black",
            activebackground='red',
            bg='#00ff00',
            command=self.thread_save_excel).grid(row=2, column=0, columnspan=2, sticky="we")

    def insert_data(self, data):
        row = (self.count,) + tuple(data)
        self.tree.insert("", tk.END, values=row)
        self.count += 1
    
    def thread_save_excel(self):
        self.excel_thread = threading.Thread(
            target=self.save_as_file)
        self.excel_thread.setDaemon(True)
        self.excel_thread.start()

    def save_as_file(self):
        lst = []
        col = [f"Channel-{i}" for i in range(33)]
        if (len(self.tree.get_children()) < 1):
            tk.messagebox.showerror(
                title="Error", message="The data is empty")

        else:
            print("Saving to Excel")
            filename = filedialog.asksaveasfilename(
                initialdir=os.getcwd(),
                title="Save To Excel",
                filetypes=(("xlsx File", "*.xlsx"), ("All Files", "*.*"))
            )

            with open('temp.csv', mode='w', newline='') as f:
                csvwriter = csv.writer(f, delimiter=',')
                for row_id in self.tree.get_children():
                    row = self.tree.item(row_id, 'values')
                    lst.append(row)
                lst = list(map(list, lst))
                lst.insert(0, col)
                for row in lst:
                    csvwriter.writerow(row)
            writer = pd.ExcelWriter(filename + '.xlsx')
            df = pd.read_csv('temp.csv', delimiter=',')
            df.to_excel(writer, 'sheetname', index=False)
            writer.save()
            tk.messagebox.showinfo(
                title="Save To Excel", message="Success Saving To Excel")
