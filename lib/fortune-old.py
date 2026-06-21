# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 13:01:06 2024

@author: JTS
"""

import os
from numbers import Number
# from collections.abc import MutableSequence
from abc import abstractmethod

# import datetime as da

from cycler import cycler
import matplotlib.pyplot as plt
import matplotlib.style as pltstyle
pltstyle.use('fast')
plt.rc('axes', prop_cycle=(cycler('color', ['r', 'g', 'b'])))
color_cycle = ['r', 'g', 'b', 'y', 'm', 'c']

# import pandas as pd
from numpy.polynomial import Polynomial as nppoly
import numpy as np


def interpret(string): 
    try: 
        return float(string)
    except ValueError: 
        return 0

class d: 
    path = os.path.dirname(os.path.abspath(__file__)) + os.sep
    with open(path + "[OP] WeatherData - GeoJSON.txt", "r") as n_archive: 
        n_data = n_archive.read()
    temperatures = [interpret(i) for i in n_data.split('\n')] # Is a list. 
    with open(path + "[OP] MaxTemp - GeoJSON.txt", "r") as m_archive: 
        m_data = m_archive.read()
    max_temperatures = [interpret(i) for i in m_data.split('\n')] # Is a list. 
    with open(path + "[OP] Rainfall - GeoJSON.txt", "r") as r_archive: 
        r_data = r_archive.read()
    rains = r_data.split('\n') # Is a list. 
    
    # Data from this one must be prepared before use. 
    # with open("WeatherData - GeoJSON.txt", "r") as archive: 
    #     _data = archive.read()
    # data = _data



class HasProperties: 
    @abstractmethod
    def __props__(self): 
        raise NotImplementedError
    def use_hint(hint): 
        def decorator(func): 
            def new_func(self, use_hints = True): 
                if use_hints and hint in self.__props__().keys(): 
                    return self.__props__()[hint]
                else: 
                    return func(self)
            return new_func
        return decorator
    
    @use_hint('period')
    def get_period(self): 
        data = np.array([[i, np.NaN][i == None] for i in self.toList()])
        print(str(data[:20]))
        data -= np.mean([i for i in data if i != None])
        # amp = 3*np.std(data)/(2**0.5)
        # data /= amp
        return len(self.toList()) / np.argmax(np.absolute(np.fft.rfft(data)))

class TimeList: # Maybe define more methods later? 
    def __init__(self, data = [], start = 0, name = None, color = None): 
        self.data = data
        self.start = start
        self.color = color
        if name == None: 
            self._id = id(self)
        else: 
            self._id = name
        self.name = 'TL - ' + str(self._id)
    def __len__(self): 
        return len(self.data)
    def keys(self): 
        return range(self.start, self.start + len(self))
    def values(self): 
        return self.data
    def __contains__(self, value): 
        return value in self.values()
    def __getitem__(self, index): 
        if isinstance(index, Number): 
            return self.data[index - self.start]
        elif isinstance(index, slice): 
            start, stop = index.start, index.stop
            if start == None: 
                start = self.start
            if stop == None: 
                start = self.start + len(self)
            return self.data[start - self.start : 
                             stop - self.start : 
                                 index.step]
    def __setitem__(self, index, value): 
        if self.data == []: 
            self.data = [value]
            self.start = index
        else: 
            if index >= len(self): 
                self.data += [None] * (index - len(self) + 1)
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

class TimeSeries(HasProperties): 
    def __init__(self, tables = [], name = None): 
        self.tables = tables
        self.props = dict()
        if name == None: 
            self._id = id(self)
        else: 
            self._id = f'"{name}"'
        self.name = 'Series - ' + str(self._id)
    def keys(self): # This and self.values() return unordered sets.
        return set.union(*[set(table.keys()) for table in self.tables])
    def values(self): # This and self.keys() return unordered sets.
        return set.union(*[set(table.values()) for table in self.tables])
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
            return TimeSeries([table[index] for table in self.tables])
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
    def predict(self, points, predictor, **kw): 
        prediction = predictor(self)
        for point in points: 
            prediction.predict(point, **kw)
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
        for axes in [(table.keys(), table.values()) for table in self.tables]: 
            plot1.plot(axes[0], axes[1], marker = ".", markersize = 1)
            # counter += 1
        return fig
    def __props__(self): 
        return self.props



# def get_pers(data): 
#     checking = 1
#     while checking < len(data): 
#         pass



def make_pred(**defaults):
    def decorate(func): 
        def out_func(self, point, data_range, save = False, **kw): 
            for item in defaults.items(): 
                if item[0] in self.props.keys(): 
                    kw.setdefault(item[0], self.props[item[0]])
                    if save: 
                        self.props[item[0]] = kw[item[0]]
                else: 
                    kw.setdefault(item[0], item[1])
                    self.props[item[0]] = kw[item[0]]
            return func(self, point, data_range, **kw)
        return out_func
    return decorate

@make_pred(period = 365, range_ = 2)
def havg_predict(self, point, data_range, **kw): 
    kw.setdefault('calc_var', False)
    period = kw['period'] # Make this stuff more elegant?
    range_ = kw['range_']
    calc_var = kw['calc_var']
    to_sum = []
    for i in range(1, range_ + 1): 
        value = self[point - (i * period)]
        to_sum.append(value)
    try: 
        out = {'value': sum(to_sum) / len(to_sum)}
    except ZeroDivisionError: 
        out = {'value': None}
    if calc_var: 
        out['var'] = max(to_sum) - min(to_sum)
    return out

class p_HistoricalAverage(TimeList): 
    def __init__(self, series): 
        TimeList.__init__(self, [])
        self.series = series
        self.p_period = series.get_period()
    def predict(self, point, range_ = 2): 
        to_sum = []
        for i in range(1, range_ + 1): 
            try: 
                value = self.series[int(point - (i * self.p_period))]
                # if value == None: 
                    # pass
            except (IndexError, KeyError): 
                pass
            else: 
                if value != None: 
                    to_sum.append(value)
        try: 
            out = sum(to_sum) / len(to_sum)
        except ZeroDivisionError: 
            print('BAD')
            out = None
        self[point] = out
        return out

@make_pred(deg = 5)
def polyfit_predict(self, point, data_range, **kw): 
    deg = kw['deg']
    stop = min(point, max(self.keys())) + 1
    back_range = range(stop - 20, stop)
    poly = nppoly.fit(back_range, [self[i] for i in back_range], deg, 
                      domain = [min(self.keys()), point + 2]) # Is this a good
                                                              # buffer?
    return {'value': poly(point)}
    

tl = TimeList(d.temperatures)
ts = TimeSeries([tl])
# ts.props['period'] = 365

# rl = TimeList(d.rains)
# rs = TimeSeries([rl])
# rs.set_pd_hints('_range', 2)

mtl = TimeList(d.max_temperatures)
mts = TimeSeries([mtl])
mts.props['period'] = 365

# new_tl = TimeList([], start = 21151)
# for i in range(21151, 21190): 
#     new_tl[i] = list(ts.predict(i, havg_predict).values())

# ts.tables.append(new_tl)

COLL = [ts, mts] # THIS IS CAPTALIZED NOW. 