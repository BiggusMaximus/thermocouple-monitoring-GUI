import tkinter as tk
from pylab import rcParams
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)
import threading
from matplotlib.figure import Figure


class graphFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padx=10, pady=10,
                         relief=tk.RIDGE, borderwidth=5, highlightthickness=2)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(sticky="nsew")

        self.fig = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.label = [f"Data {i}" for i in range(1,33)]
        self.data = {}
        self.lower_limit = -5
        self.upper_limit = 5
        self.threshold = 100
        self.count = 0
        self.data["count"] = []

        for i in range(0, 32):
            self.data[i] = []
    
    def update_graph(self, data):
        self.ax.clear()
        self.ax.grid()
        self.data["count"].append(self.count)
        for i in range(0, 32):    
            if isinstance(data[i], str):
                self.data[i].append(0)
            else: 
                if data[i] > self.upper_limit:
                    self.upper_limit = data[i] + 10
                
                if data[i] < self.lower_limit:
                    self.upper_limit = data[i] - 10
                
                self.ax.set_ylim([ self.lower_limit, self.upper_limit])
                self.data[i].append(data[i])
               

                if self.count > self.threshold:
                    self.ax.plot(self.data["count"][-self.threshold:] , self.data[i][-self.threshold:], label=self.label[i])
                else:
                    self.ax.plot(self.data["count"] , self.data[i], label=self.label[i])
                
                self.ax.legend()    
        self.count +=  1
        self.canvas.draw()

