# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 09:29:51 2024

@author: JTS
"""

import sys # Save standard I/O so we can reset it on exit. 
_stdout = sys.stdout
_stderr = sys.stderr
_stdin = sys.stdin

from lib import *


# GUI #


from tkinter import *
# from tkinter import ttk
from SubWindows import Console, Graph, Structure

root = Tk()  # create root window
root.title("U Oracle")
# root.maxsize(900,  600)  # width x height
root.config(bg="skyblue")

for x in range(3): 
    root.columnconfigure(x, weight = 1)
for y in range(2): 
    root.rowconfigure(y, weight = 1)


# Stolen Toolbar Widget #

class Toolbar(Frame):
    def __init__(self):
        super().__init__()
        # self.master = master
        self.initUI()
        
    def initUI(self):
        # self.master.title("Submenu")
        
        menubar = Menu(self.master)
        self.master.config(menu=menubar)
        
        fileMenu = Menu(menubar)
        
        submenu = Menu(fileMenu)
        submenu.add_command(label="Dataset")
        # submenu.add_command(label="Bookmarks")
        # submenu.add_command(label="Mail")
        fileMenu.add_cascade(label='Import', menu=submenu, underline=0)
        
        fileMenu.add_separator()
        
        fileMenu.add_command(label="Exit", underline=0, command=self.onExit)
        menubar.add_cascade(label="File", underline=0, menu=fileMenu)
    
    def onExit(self):
        self.master.destroy()


# Setup all the windows and deal with panes #

# TopBar = Frame(root, height = 10, bg = 'white')
# TopBar.pack(fill = X, side = TOP)

Pane1 = PanedWindow(orient = HORIZONTAL, sashwidth = 10, bg = "#555555")
Pane1.pack(fill = BOTH, expand = True, side = BOTTOM)

PredictionWindow = Frame(Pane1, bg = 'white')
Pane1.add(PredictionWindow)

Pane2 = PanedWindow(orient = VERTICAL, sashwidth = 10, bg = "#555555")
Pane1.add(Pane2)

Pane3 = PanedWindow(orient = HORIZONTAL, sashwidth = 10, bg = "#555555")
Pane2.add(Pane3)

PythonWindow = Frame(Pane2, bg = 'white')
Pane2.add(PythonWindow)

GraphWindow = Frame(Pane3, bg = 'white')
Pane3.add(GraphWindow)

DataWindow = Frame(Pane3, bg = 'white', width = 100)
Pane3.add(DataWindow)

# PredictionWindow = Frame(root, bg = 'white')
# PredictionWindow.grid(column = 0, row = 0, padx = 10, pady = 10, 
#                       sticky = 'news', rowspan = 2)

# GraphWindow = Frame(root, bg = 'white')
# GraphWindow.grid(column = 1, row = 0, padx = 10, pady = 10, 
#                   sticky = 'news')

# PythonWindow = Frame(root, bg = 'white')
# PythonWindow.grid(column = 1, row = 1, padx = 10, pady = 10, 
#                   sticky = 'news', columnspan = 2)

# DataWindow = Frame(root, bg = 'white')
# DataWindow.grid(column = 2, row = 0, padx = 10, pady = 10, 
#                 sticky = 'news')

MenuToolbar = Toolbar()
# MenuToolbar.pack()

PythonConsole = Console(PythonWindow, locals(), root.destroy)
PythonConsole.pack(fill = BOTH, expand = True)


class _global_graphndata: 
    def __init__(self): 
        self.GraphContainer = Frame(GraphWindow, bg = 'white')
        self.GraphContainer.pack()
        self.PlotGraph = Graph(self.GraphContainer, COLL)
        self.PlotGraph.pack()
        
        # testbtn = Button(PredictionWindow, text = "THIS IS A BUTTON", 
        # width = 10, 
        #                  height = 100)
        # testbtn.pack(fill = BOTH, expand = True)
        
        self.DataStructure = Structure(DataWindow, COLL)
        self.DataStructure.pack(fill = BOTH, expand = True)
    
    def update_widgets(self): 
        self.GraphContainer.destroy()
        self.GraphContainer = Frame(GraphWindow, bg = 'white')
        self.GraphContainer.pack()
        self.PlotGraph = Graph(self.GraphContainer, COLL)
        self.PlotGraph.pack()
        
        self.DataStructure.destroy()
        self.DataStructure = Structure(DataWindow, COLL)
        self.DataStructure.pack(fill = BOTH, expand = True)

globgrand = _global_graphndata()

# _global_graphndata = [GraphContainer, PlotGraph, DataStructure]

# def update_widgets(): 
#     # def del_GraphContainer(): 
#     #     global GraphContainer
#     #     GraphContainer.destroy()
#     #     del_GraphContainer()
#     # global GraphContainer
#     # GraphContainer = Frame(GraphWindow, bg = 'white')
#     # GraphContainer.pack()
#     # global PlotGraph
#     # PlotGraph = Graph(GraphWindow, COLL)
#     # PlotGraph.pack()
    
#     # def del_DataStructure(): 
#     #     global DataStructure
#     #     DataStructure.destroy()
#     # del_DataStructure()
#     # global DataStructure
#     # DataStructure = Structure(DataWindow, COLL)
#     # DataStructure.pack(fill = BOTH, expand = True)
    
#     global _global_graphndata
#     for widget in _global_graphndata: 
#         widget.destroy()
    
#     global GraphContainer
#     GraphContainer = Frame(GraphWindow, bg = 'white')
#     GraphContainer.pack()
    
#     global PlotGraph
#     PlotGraph = Graph(GraphWindow, COLL)
#     PlotGraph.pack()
    
#     global DataStructure
#     DataStructure = Structure(DataWindow, COLL)
#     DataStructure.pack(fill = BOTH, expand = True)
    
#     _global_graphndata = [GraphContainer, PlotGraph, DataStructure]

def pred_popup(pred): 
    popup = Toplevel(root)
    popup.geometry("750x250")
    popup.title("Prediction Popup")
    series_txt = Label(popup, text = "Select Data Series: ")
    series_txt.grid(row = 0, column = 0, padx = 10, pady = 10)
    
    options = ["<Choose>"] + [series.name for series in COLL]
    
    # datatype of menu text 
    clicked = StringVar() 
      
    # initial menu text 
    clicked.set( "<Choose>" ) 
    
    series_drop = OptionMenu(popup, clicked, *options ) 
    series_drop.grid(row = 0, column = 1)
    
    data_range_txt = Label(popup, text = "Define the Data Range: ")
    data_range_txt.grid(row = 1, column = 0)
    
    data_range_in = Text(popup, width = 20, height = 1)
    data_range_in.grid(row = 1, column = 1)
    data_range_in.insert("end-1c", 'all')
    
    data_range_ex = Label(popup, text = "lower, upper (e.g. 110, 150)")
    data_range_ex.grid(row = 1, column = 2, padx = 10, pady = 10)
    
    prediction_range_txt = Label(popup, text = "Define the Prediction Range: ")
    prediction_range_txt.grid(row = 2, column = 0)
    
    pred_range_in = Text(popup, width = 20, height = 1)
    pred_range_in.grid(row = 2, column = 1)
    
    overrides_txt = Label(popup, text = "Overrides (Optional): ")
    overrides_txt.grid(row = 3, column = 0)
    
    overrides_in = Text(popup, width = 20, height = 1)
    overrides_in.grid(row = 3, column = 1)
    overrides_in.insert('end-1c', '{}')
    
    overrides_note = Label(popup, text = "Note: Only use this one if you know "
                           "what you're doing! ")
    overrides_note.grid(row = 3, column = 2, padx = 10, pady = 10)
    
    def popup_predict(): 
        series = clicked.get()
        data_range = data_range_in.get(1.0, 'end-1c')
        pred_range = pred_range_in.get(1.0, 'end-1c')
        overrides = overrides_in.get(1.0, 'end-1c')
        
        if series == "<Choose>" or pred_range == '': 
            warning_txt = Label(popup, text = "Enter a data series and "
                                "prediction range! ", fg = 'red')
            warning_txt.grid(row = 4, column = 1)
            return False
        else: 
            series_actual = [i for i in COLL if i.name == series]
            assert len(series_actual) == 1
            series_actual = series_actual[0]
            
            if data_range == 'all': 
                data_range_actual = [None, None]
            else: 
                data_range_actual = [eval(i.strip()) for i in 
                                     data_range.split(',')]
                assert len(data_range_actual) == 2 # THIS IS IN ELSE
            
            pred_range_actual = [int(i.strip()) for i in 
                                 pred_range.split(',')]
            assert len(pred_range_actual) == 2
            
            overrides_actual = eval(overrides, globals(), locals())
            assert isinstance(overrides_actual, dict)
            
            # new_tl = TimeList([], start = pred_range_actual[0])
            # for i in range(*pred_range_actual): 
            #     # This uses the nonlocal var 'pred'. 
            #     new_tl[i] = series_actual.predict(i, pred)['value']
            new_tl = series_actual.get_prediction(
                range(*pred_range_actual), 
                pred, 
                data_range = slice(*data_range_actual), 
                **overrides_actual)
            series_actual.tables.append(new_tl)
            
            # new_series = TimeSeries([new_tl])
            # COLL.append(new_series)
            # series_actual.tables.append(new_tl)
            popup.destroy()
            globgrand.update_widgets()
    
    pred_btn = Button(popup, text = "Predict! ", command = popup_predict)
    pred_btn.grid(row = 4, column = 0, padx = 10, pady = 10)

PredictionWindow.grid_columnconfigure(0, weight=1)

havg_btn = Button(PredictionWindow, text = "Historical Average", width = 40,
                 height = 5, command = lambda: pred_popup(p_HistoricalAverage))
# havg_btn.pack(fill = X, expand = True, side = TOP)
havg_btn.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = EW)

polyfit_btn = Button(PredictionWindow, text = "Polynomial Fit", width = 40,
                     height = 5, command = lambda: pred_popup(p_PolyFit))
polyfit_btn.grid(row = 1, column = 0, padx = 10, pady = 10, sticky = EW)

# curvefit_btn = Button(PredictionWindow, text = "Curve Fit", width = 40,
#                      height = 5, command = lambda: pred_popup(p_CurveFit))
# curvefit_btn.grid(row = 2, column = 0, padx = 10, pady = 10, sticky = EW)

expofit_btn = Button(PredictionWindow, text = "Exponential Fit", width = 40,
                     height = 5, command = lambda: pred_popup(p_ExpoFit))
expofit_btn.grid(row = 2, column = 0, padx = 10, pady = 10, sticky = EW)

logfit_btn = Button(PredictionWindow, text = "Logarithmic Fit", width = 40,
                    height = 5, command = lambda: pred_popup(p_LogFit))
logfit_btn.grid(row = 3, column = 0, padx = 10, pady = 10, sticky = EW)

powerfit_btn = Button(PredictionWindow, text = "Power Law Fit", width = 40,
                    height = 5, command = lambda: pred_popup(p_PowerFit))
powerfit_btn.grid(row = 4, column = 0, padx = 10, pady = 10, sticky = EW)



# import code
# code.interact()

def on_exit(): 
    sys.stdout = _stdout
    sys.stderr = _stderr
    sys.stdin = _stdin
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_exit) # Doesn't quite work as expected. 
                                           # TODO Maybe?
root.mainloop()