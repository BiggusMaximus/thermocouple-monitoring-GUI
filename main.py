import tkinter as tk
from table import *
from plotting import *
from connection import *
from data import *
from tkinter import ttk, filedialog, messagebox
import sys
from itertools import groupby



class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Modbus Potter - UPN Veteran Jakarta")
        #self.state('zoomed')
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=20)
        self.rowconfigure(0, weight=8)
        self.rowconfigure(1, weight=1)
        self.protocol("WM_DELETE_WINDOW", self.closeWindow)
        self.iconbitmap('icon.ico')

        self.data = {}
        self.count_number = 0
        #self.create_menu()
        self.create_child_frames()
        self.get_data()
        self.checked_data = ["-"] * 32

    def create_menu(self):
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save", command=self.save_file)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.closeWindow)
        menubar.add_cascade(label="File", menu=filemenu)
        self.config(menu=menubar)

    def create_child_frames(self):
        self.data_frame = dataFrame(self, self.data)
        self.graph_frame = graphFrame(self)
        self.table_frame = tableFrame(self)
        self.connection_frame = connectionFrame(self, self.data)

        # Assign grid positions to the child frames
        self.connection_frame.grid(
            row=0, column=0, sticky="nsew", padx=(10, 10), pady=(10, 10))
        self.data_frame.grid(row=0, column=1, sticky="nsew",
                             padx=(10, 10), pady=(10, 10))
        self.table_frame.grid(row=1, column=0, columnspan=3,
                              sticky="nsew", padx=(10, 10), pady=(10, 10))

        self.graph_frame.grid(
            row=0, column=2, sticky="nsew", padx=(10, 10), pady=(10, 10))

    def save_file(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.data_frame.title_label['text'])
                messagebox.showinfo(
                    "File Saved", "Data frame saved successfully!")

    def closeWindow(self):
        if messagebox.askyesnocancel("Quit?", "Do you sure you want to quit?"):
            self.quit()
            self.destroy()
            sys.exit()
    
    def check_same_items(self, lst):
        if len(lst) < 2:  # If the list has less than 2 items, all items are the same
            return True

        first_item = lst[0]
        for item in lst[1:]:
            if item != first_item:
                return False

        return True

    def get_data(self):
        collect_data_status = True
        #print(f"{self.connection_frame.connected_status}, {self.connection_frame.isStart_status}, {self.count_number}, {collect_data_status}")
        timing = self.connection_frame.TIMING[self.connection_frame.TIMING_LIST.index(self.connection_frame.timing_value.get())]
        if ((self.connection_frame.connected_status) and (self.connection_frame.isStart_status)):
            if self.count_number < timing:
                result = self.connection_frame.client.read_holding_registers(
                    address=0x0,
                    count=0x20,
                    unit=0x1
                )
                datas = result.registers
                

                for i in range(16):
                    if self.data_frame.checkbox_value_16[i].get():
                        if datas[i] > 1000:
                            pass
                        else:
                            #print(f"Channel-{i} : {self.data_frame.checkbox_value_16[i].get()}, {type(self.data_frame.checkbox_value_16[i].get())}")
                            self.checked_data[i] = datas[i]/10
                            self.data_frame.data_labels[i][0].config(
                                text=datas[i]/10)
                    else:
                        pass

                    # Unchecked
                    if self.data_frame.checkbox_value_32[i].get():
                        #print(f"Channel-{i} : {self.data_frame.checkbox_value_32[i].get()}, {type(self.data_frame.checkbox_value_32[i].get())}")
                        if datas[i+16] > 1000:
                            pass
                        else:
                            self.data_frame.data_labels[i][1].config(
                                text=datas[i+16]/10
                            )
                            self.checked_data[i+16] = datas[i+16]/10
                    else:
                        pass
                    
                self.table_frame.insert_data(data=self.checked_data)
                self.graph_frame.update_graph(self.checked_data)
                self.count_number += 1
            else:
                collect_data_status = False
        else:
            self.after(1000, self.get_data)
    
        if self.count_number > 0:
            if collect_data_status:
                self.after(1000, self.get_data)
            else:
                self.count_number = 0
                collect_data_status = True
                self.connection_frame.stop_button.configure(state="disabled", bg='red')
                self.connection_frame.start_button.configure(state="normal", bg='#00ff00')
                self.connection_frame.isStart_status = False
                self.checked_data = ["-"]*32
                messagebox.showinfo("Data Acquisition", f"Finish Collect {self.connection_frame.timing_value.get()} data")

                self.after(1000, self.get_data)

if __name__ == "__main__":
    app = App()
    app.mainloop()
