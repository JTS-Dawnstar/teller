# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 12:54:20 2024

@author: JTS

With some parts borrowed from: 
https://github.com/kurawlefaraaz/Tk-Themed-Utilities/blob/main/EditableTreeview.py
"""

from tkinter import * 
import tkinter as tk # TODO: Consolidate these into a single import. 
 
# Importing ttk from tkinter
from tkinter import ttk

class PopupEntry(tk.Entry):
    def __init__(self, parent, x, y, textvar,width = 10 ,entry_value='', 
                 text_justify = 'left', ):
        super().__init__(parent, relief = 'flat', justify = text_justify, 
                         bg='white', textvariable=textvar, font= "sublime ")
        self.place(x=x, y=y, width=width)
        
        self.textvar = textvar
        self.textvar.set(entry_value)
        self.focus_set()
        self.select_range(0, 'end')
        # move cursor to the end
        self.icursor('end')

        self.wait_var = tk.StringVar(master=self)
        self._bind_widget()

        self.entry_value = entry_value
        self.wait_window()
    
    def _bind_widget(self):
        self.bind("<Return>", self.retrive_value)
        self.bind('<FocusOut>', self.retrive_value)

    def retrive_value(self, e):
        value = self.textvar.get()
        self.destroy()
        self.textvar.set(value)
 
            
# def demo():

#     root = tk.Tk()
#     root.title('Demo')
#     root.geometry('620x200')

#     PopupEntry(root,0,0,tk.StringVar(),width=200)
#     root.mainloop()

# if __name__ == '__main__':

#     demo()

class EditableTreeview(ttk.Treeview):
    def __init__(self, parent, columns, bind_key, data:list, 
                 non_editable_columns = "", collection = None):
        super().__init__(parent, columns=columns)
        self.collection = collection
        self.parent = parent
        self.column_name = columns
        self.data = data
        self.bind_key = bind_key
        self.non_editable_columns = non_editable_columns

        # self.set_primary_key_column_attributes()
        self.set_headings()
        self.insert_data()
        self.set_edit_bind_key()
    
    def set_primary_key_column_attributes(self):
        self.column("#0",width=100,stretch=1)

    def set_headings(self):
        for i in self.column_name:
            # print(str(i))
            self.heading(column=i, text=i)

    def insert_data(self):
        for values in self.data:
            self.insert('', tk.END, text = 'three', values=values)
    
    def set_edit_bind_key(self):
        self.bind('<Double Button-1>', self.edit)

    def get_absolute_x_cord(self):
        rootx = self.winfo_pointerx()
        widgetx = self.winfo_rootx()

        x = rootx - widgetx

        return x

    def get_absolute_y_cord(self):
        rooty = self.winfo_pointery()
        widgety = self.winfo_rooty()

        y = rooty - widgety

        return y
    
    def get_current_column(self):
        pointer = self.get_absolute_x_cord()
        return self.identify_column(pointer)

    def get_cell_cords(self,row,column):
        return self.bbox(row, column=column)
    
    def get_selected_cell_cords(self):
        row = self.focus()
        column = self.get_current_column()
        return self.get_cell_cords(row = row, column = column)

    def update_row(self, values, current_row, currentindex):
        # try: 
        #     self.parent.state()
        # except: 
        #     print("State went wrong. ")
        #     return None

        # self.delete(current_row)
        
        # # Put it back in with the upated values
        # self.insert('', currentindex, text = text, values = values)
        
        self.item(current_row, values=values)

    def check_region(self):
        result = self.identify_region(x=(self.winfo_pointerx() - 
                                         self.winfo_rootx()), 
                                      y=(self.winfo_pointery()  - 
                                         self.winfo_rooty()))
        # print(result)
        if result == 'cell':return True
        else: return False

    def check_non_editable(self):
        if self.get_current_column() in self.non_editable_columns:return False
        else: return True

    def edit(self, e):
        if self.check_region() == False: return
        elif self.check_non_editable() == False: return
        
        current_row = self.focus()
        print("Current_row: " + str(current_row) + " - " + 
              str(type(current_row)))
        currentindex = self.index(self.focus())
        print("Currentindex: " + str(currentindex))
        current_row_values = list(self.item(self.focus(),'values'))
        current_column = int(self.get_current_column().replace("#",''))-1
        try:
            current_cell_value = current_row_values[current_column]
        except IndexError: 
            return None # Basically just halt. 
        
        entry_cord = self.get_selected_cell_cords()
        entry_x = entry_cord[0]
        entry_y = entry_cord[1]
        entry_w = entry_cord[2]
        entry_h = entry_cord[3]
        
        entry_var = tk.StringVar()
        
        PopupEntry(self, x=entry_x, y=entry_y, width=entry_w, 
                   entry_value=current_cell_value, textvar= entry_var, 
                   text_justify='left')
        
        if entry_var.get() != current_cell_value:
            current_row_values[current_column] = entry_var.get()
            # print(str(current_row_values[current_column]))
            self.update_row(values=current_row_values, current_row=current_row, 
                            currentindex=currentindex)
            # _parent = ttk.Treeview.parent
            # print(str(_parent(self, _parent(self, self.focus()))))
            # print(str(_parent(self, self.focus())))
            parent = ttk.Treeview.parent(self, self.focus())
            if parent.endswith('properties'): 
                _iid = parent[:len(parent) - 10]
                parent_series = [i for i in self.collection if str(id(i)) == 
                                 _iid][0]
                # parent_series.set_pd_hints()
                # print(self.item(current_row))
                # parent_series.set_pd_hints(self.item(current_row)['text'], 
                #                            int(current_row_values[0]))
                parent_series.props[self.item(current_row)['text']
                                       ] = int(current_row_values[0])
            

# Stuff below here is original now. #

class Structure(EditableTreeview): 
    def __init__(self, master, collection): # collection should be list. 
        super().__init__(master, columns = ("value",), 
                         bind_key='<Double-Button-1>', data = [], 
                         collection = collection)
        
        # self.collection = collection
        self.heading("#0", text = "Structure")
        self.heading("value", text = "Value")
        self.update()
    def update(self): 
        self.delete(*self.get_children())
        for item in self.collection: 
            self.insert('', END, iid = id(item), text = item.name)
            if hasattr(item, "tables"): 
                self.insert(id(item), END, iid = str(id(item)) + 'properties', 
                            text = "Properties")
                for hint in item.props.keys(): 
                    self.insert(str(id(item)) + 'properties', END, text = hint, 
                                values = (str(item.props[hint])))
                for subitem in item.tables: 
                    self.insert(id(item), END, iid = id(subitem), 
                                text = subitem.name)
                    self.insert(id(subitem), END, iid = str(id(subitem)) + 
                                'data', text = "Data")
            else: 
                self.insert(id(item), END, iid = str(id(item)) + 'data', 
                            text = "Data")
