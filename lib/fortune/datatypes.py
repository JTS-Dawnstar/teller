from .properties import HasProperties

from numbers import Number

from cycler import cycler
import matplotlib.pyplot as plt
import matplotlib.style as pltstyle
pltstyle.use('fast')
plt.rc('axes', prop_cycle=(cycler('color', ['r', 'g', 'b'])))
color_cycle = ['r', 'g', 'b', 'y', 'm', 'c']

# class DisplacedList: 
#     def __init__(self, data = [], start = 0): 
#         self.data = data
#         self.start = start
#     def __getitem__(self, index): 
#         if isinstance(index, Number): 
#             return self.data[index - self.start]
#         elif isinstance(index, slice): 
#             start, stop = index.start, index.stop
#             if start == None: 
#                 start = self.start
#             if stop == None: 
#                 start = self.start + len(self)
#             return self.data[start - self.start : 
#                              stop - self.start : 
#                                  index.step]
#     def __setitem__(self, key, value): 
#         if self.data == []: 
#             self.data = [value]
#             self.start = key
#         else: 
#             if key >= len(self): 
#                 self.data += [None] * (key - len(self) + 1)
#             elif key < self.start: 
#                 self.data = [None] * (self.start - key) + self.data
#                 self.start = key
#             self.data[key - self.start] = value

class AddName_ID: 
    def __init__(self, name = None): 
        if name == None: 
            self._id = id(self)
        else: 
            self._id = f'"{name}"'
        self.name = type(self).__name__ + ' - ' + str(self._id)

class TimeList(AddName_ID): # Maybe define more methods later? 
    def __init__(self, data = [], start = 0, name = None): 
        AddName_ID.__init__(self, name = name)
        self.data = data
        self.start = start
        # if name == None: 
        #     self._id = id(self)
        # else: 
        #     self._id = name
        # self.name = 'TL - ' + str(self._id)
    def __len__(self): 
        return len(self.data)
    def keys(self): 
        return range(self.start, self.start + len(self))
    def values(self): 
        return self.data
    def toAxes(self): 
        x = []
        y = []
        for key in self.keys(): 
            if self[key] != None: 
                x.append(key)
                y.append(self[key])
        return (x, y)
    def __contains__(self, value): 
        return value in self.values()
    def __getitem__(self, index): 
        if isinstance(index, Number): 
            return self.data[index - self.start]
        elif isinstance(index, slice): # slice.step not supported
            start, stop = index.start, index.stop
            if start != None: 
                start -= self.start
            if stop != None: 
                stop -= self.start
            if start == None: 
                argstart = self.start
            else: 
                argstart = index.start
            # And yes, we DO need self.__class__ for this. Think subclassing. 
            if hasattr(self, 'series'): 
                return self.__class__(self.data[start : stop], self.series, 
                                      start = argstart)
            else: 
                return self.__class__(self.data[start : stop], 
                                      start = argstart)
    def __setitem__(self, index, value): 
        if self.data == []: 
            self.data = [value]
            self.start = index
        else: 
            if index >= self.start + len(self) - 1: 
                self.data += [None] * (index - len(self) - self.start + 1)
            elif index < self.start: 
                self.data = [None] * (self.start - index) + self.data
                self.start = index
            self.data[index - self.start] = value
    def insert(self, index, value): 
        self.data.insert(index - self.start, value)
    def append(self, value): 
        self[self.start + len(self)] = value
    def count(self, value): 
        return self.data.count(value)

# class TimeList(MutableSequence): 
#     def __int__(self, data, start = 0, name = None): 
#         pass

class TimeSeries(HasProperties, AddName_ID): 
    def __init__(self, tables = [], name = None): 
        AddName_ID.__init__(self, name = name)
        self.tables = tables
        self.props = dict()
        # if name == None: 
        #     self._id = id(self)
        # else: 
        #     self._id = f'"{name}"'
        # self.name = 'Series - ' + str(self._id)
    def keys(self): # This and self.values() return unordered sets.
        return set.union(*[set(table.keys()) for table in self.tables])
    def values(self): # This and self.keys() return unordered sets.
        return set.union(*[set(table.values()) for table in self.tables])
    def toAxes(self): 
        x = []
        y = []
        for key in sorted(self.keys()): 
            if self[key] != None: 
                x.append(key)
                y.append(self[key])
        return (x, y)
    def toList(self): 
        return [self[i] for i in sorted(self.keys())]
    def __contains__(self, value): 
        return value in self.values()
    def __getitem__(self, index): 
        if isinstance(index, Number): 
            for table in self.tables: 
                if index in table.keys(): 
                    return table[index]
            # else: 
            raise KeyError(str(index))
        elif isinstance(index, slice): 
            out = TimeSeries([table[index] for table in self.tables])
            out.props = self.props.copy()
            return out
    def get_table(self, _id): 
        return [table for table in self.tables if table._id == _id][0]
    # def predict(self, point, predictor, data_range = "all", save = False, 
    #             **kw): 
    #     if data_range == "all": 
    #         data_range = slice(None)
    #     prediction = predictor(self, point, data_range = data_range, **kw)
    #     if save != False: 
    #         save[point] = [prediction['value'], set(prediction['flags'])]
    #     return prediction
    def get_prediction(self, points, predictor, data_range = 'all', 
                       **overrides): 
        # if data_range == 'all': 
        #     data_arg = self
        # else: 
        #     data_arg = self[data_range]
        data_arg = self[data_range]
        prediction = predictor([], data_arg)
        for key, value in overrides.items(): 
            setattr(prediction, key, value)
        for point in points: 
            prediction.predict(point)
        return prediction
    def plot(self, style = 'o', dpi = 160): 
        # x_axis = self.keys()
        # y_axis = self.values()
        plt.figure(figsize = (15, 6), dpi = dpi)
        counter = 0
        for axes in [(table.keys(), table.values()) for table in self.tables]: 
            plt.plot(axes[0], axes[1], style + color_cycle[counter % 6], 
                     markersize = 1)
            counter += 1
    def plot_embed(self, style = 'o', dpi = 160, figsize = (5, 2), 
                   figsubplot = None): 
        # x_axis = self.keys()
        # y_axis = self.values()
        if figsubplot == None: 
            fig = plt.Figure(figsize = figsize, dpi = dpi)
            plot1 = fig.add_subplot(111)
        else: 
            fig = figsubplot[0]
            plot1 = figsubplot[1]
        # counter = 0
        # for axes in [(table.keys(), table.values()) for table in self.tables]: 
        #     plot1.plot(axes[0], axes[1], marker = ".", markersize = 1)
        for axes in [table.toAxes() for table in self.tables]: 
            plot1.plot(axes[0], axes[1], marker = ".", markersize = 1)
            # counter += 1
        return fig
    def __props__(self): 
        return self.props
