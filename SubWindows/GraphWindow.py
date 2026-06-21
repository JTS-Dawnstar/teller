# -*- coding: utf-8 -*-
"""
Created on Sun Jun  9 11:15:20 2024

@author: JTS, cosine 1509 at geeksforgeeks.org

Based off of a geeksforgeeks tutorial: 
https://www.geeksforgeeks.org/how-to-embed-matplotlib-charts-in-tkinter-gui/
"""

from tkinter import * 
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk) 
  
# plot function is created for  
# plotting the graph in  
# tkinter window 
# def plot(): 
  
#     # the figure that will contain the plot 
#     fig = Figure(figsize = (5, 5), 
#                  dpi = 100) 
  
#     # list of squares 
#     y = [i**2 for i in range(101)] 
  
#     # adding the subplot 
#     plot1 = fig.add_subplot(111)
  
#     # plotting the graph 
#     plot1.plot(y) 
  
#     # creating the Tkinter canvas 
#     # containing the Matplotlib figure 
#     canvas = FigureCanvasTkAgg(fig, 
#                                master = window)   
#     canvas.draw() 
  
#     # placing the canvas on the Tkinter window 
#     canvas.get_tk_widget().pack() 
  
#     # creating the Matplotlib toolbar 
#     toolbar = NavigationToolbar2Tk(canvas, 
#                                    window) 
#     toolbar.update() 
  
#     # placing the toolbar on the Tkinter window 
#     canvas.get_tk_widget().pack() 

class Graph(Frame): 
    def __init__(self, parent, data, test = False): # data is [series1, 
                                                    # series 2, ...]
        super().__init__(parent)
        
        if test: 
            self.fig = Figure(figsize = (5, 5), 
                          dpi = 100) 
            
            # list of squares 
            y = [i**2 for i in range(101)] 
            
            # adding the subplot 
            plot1 = self.fig.add_subplot(111)
            
            # plotting the graph 
            plot1.plot(y) 
        else: 
            self.fig = Figure(figsize = (10, 4), 
                          dpi = 100)
            self.plot1 = self.fig.add_subplot(111)
            for series in data: 
                self.fig = series.plot_embed(figsubplot = (self.fig, 
                                                           self.plot1))
        
        # creating the Tkinter canvas 
        # containing the Matplotlib figure 
        self.canvas = FigureCanvasTkAgg(self.fig, master = parent)
        
        # creating the Matplotlib toolbar 
        self.toolbar = NavigationToolbar2Tk(self.canvas, parent) 
        
    def pack(self): 
        self.canvas.draw()
        
        # placing the canvas on the Tkinter window 
        self.canvas.get_tk_widget().pack() 
        
        self.toolbar.update()
        
        # placing the toolbar on the Tkinter window 
        self.canvas.get_tk_widget().pack() 
    
    # def destroy(self): 
    #     self.fig.clear()
    #     Frame.destroy(self)

# # the main Tkinter window 
# window = Tk() 
  
# # setting the title  
# window.title('Plotting in Tkinter') 
  
# # dimensions of the main window 
# window.geometry("500x500") 
  
# # button that displays the plot 
# plot_button = Button(master = window,  
#                       command = plot, 
#                       height = 2,  
#                       width = 10, 
#                       text = "Plot") 
  
# # place the button  
# # in main window 
# plot_button.pack() 
  
# # run the gui 
# window.mainloop()

if __name__ == "__main__": 
    root = Tk()
    graph = Graph(root, None, test = True)
    graph.pack(fill=BOTH, expand=True)
    root.mainloop()
    