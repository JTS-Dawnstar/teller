from .datatypes import TimeList
# from abc import abstractmethod, ABCMeta
from numpy.polynomial import Polynomial as nppoly
import numpy as np
# import scipy.optimize as scpop

class Predictor(TimeList): 
    def __init__(self, data, series, start = 0): 
        TimeList.__init__(self, data, start = start)
        self.series = series
    # @staticmethod
    # @abstractmethod
    # def requirements():
    #     raise NotImplementedError

class p_HistoricalAverage(Predictor): 
    def __init__(self, data, series, start = 0): 
        Predictor.__init__(self, data, series, start)
        self.p_period = series.get_period()
        
        self._cache_range = range(-5, 0)
    def predict(self, point): 
        to_sum = []
        for i in self._cache_range: 
            index = int(point + (i * self.p_period))
            keys = self.series.keys()
            value = None
            if index in keys: 
                value = self.series[index]
            if value != None: # value could be None even if 'index in keys'. 
                to_sum.append(value)
        try: 
            out = sum(to_sum) / len(to_sum)
        except ZeroDivisionError: 
            # print('BAD')
            out = None
        self[point] = out
        return out
    # @staticmethod
    # def requirements(): # Do we actually need this? Wouldn't be so sure. 
    #     return {'Period': 'p_period'}

class p_PolyFit(Predictor): 
    def __init__(self, data, series, start = 0): 
        Predictor.__init__(self, data, series, start)
        self.p_deg = series.get_deg()
        
        self._cache_poly = (None, None) # (p_deg, poly)
    def get_poly(self): 
        if self._cache_poly[0] != self.p_deg: 
            self._cache_poly = (self.p_deg, 
                              nppoly.fit(*self.series.toAxes(), 
                                         deg = self.p_deg))
        return self._cache_poly[1]
    def predict(self, point): 
        out = self.get_poly()(point)
        self[point] = out
        return out
    # @staticmethod
    # def requirements(): 
    #     return {'Degree': 'p_deg'}

class p_ExpoFit(Predictor): 
    def __init__(self, data, series, start = 0): 
        Predictor.__init__(self, data, series, start)
        self.p_tone = series.get_tone()
        if self.p_tone == 1: 
            self.p_asymp = min(self.series.values())
        else: 
            self.p_asymp = max(self.series.values())
        self.p_epsilon = (max(self.series.values()) - 
                          min(self.series.values())) / 1000 # Good buffer? 
        
        # print(f'p_tone: {self.p_tone}')
        # print(f'p_asymp: {self.p_asymp}')
        
        # self._cache_vstretch, self._cache_hcomp = self.get_expo()
        self._cache_expo = [None, None, None] # p_tone, p_asymp, params
    def get_expo(self): # Mostly stolen from https://stackoverflow.com/
                        # questions/3433486/how-to-do-exponential-and-
                        # logarithmic-curve-fitting-in-python-i-found-only-poly. 
                        # Ben's Answer. Fixes the issue with the weights too. 
        if (self._cache_expo[0] != self.p_tone or 
            self._cache_expo[1] != self.p_asymp): 
            self._cache_expo = [self.p_tone, self.p_asymp, None]
            
            xs, ys = self.series.toAxes()
            ys = [i - self.p_asymp for i in ys] 
            if self.p_tone == -1: 
                ys = [-i for i in ys]
            ys = [i + self.p_epsilon for i in ys]
            # print(ys[:50])
            
            S_x2_y = 0.0
            S_y_lny = 0.0
            S_x_y = 0.0
            S_x_y_lny = 0.0
            S_y = 0.0
            for (x, y) in zip(xs, ys):
                S_x2_y += x * x * y
                S_y_lny += y * np.log(y)
                S_x_y += x * y
                S_x_y_lny += x * y * np.log(y)
                S_y += y
            
            a = (S_x2_y * S_y_lny - S_x_y * S_x_y_lny) / (S_y * S_x2_y - S_x_y  
                                                          * S_x_y)
            b = (S_y * S_x_y_lny - S_x_y * S_y_lny) / (S_y * S_x2_y - S_x_y * 
                                                       S_x_y)
            
            self._cache_expo[2] = [a, b]
        a, b = self._cache_expo[2]
        return lambda x: (self.p_tone * (np.exp(a) * np.exp(b * x) - 
                                         self.p_epsilon) + self.p_asymp)
    def predict(self, point): 
        out = self.get_expo()(point)
        self[point] = out
        return out

class p_LogFit(Predictor): 
    def __init__(self, data, series, start = 0): 
        Predictor.__init__(self, data, series, start)
        self.p_vasymp = min(self.series.keys()) - 1 # Good default? 
        
        self._cache_log = [None, None] # p_vasymp, params
    def get_log(self): # Same source as with p_ExpoFit. But i coded it this 
                       # time. 
        if self._cache_log[0] != self.p_vasymp: 
            self._cache_log[0] = self.p_vasymp
            
            xs, ys = self.series.toAxes()
            xs = [i - self.p_vasymp for i in xs]
            
            S_y_lnx = 0
            S_y = 0
            S_lnx = 0
            S_lnx2 = 0
            for (x, y) in zip(xs, ys): 
                S_y_lnx += y * np.log(x)
                S_y += y
                S_lnx += np.log(x)
                S_lnx2 += np.log(x) ** 2
            
            n = len(xs)
            b = ((n * S_y_lnx) - (S_y * S_lnx)) / ((n * S_lnx2) - (S_lnx ** 2))
            a = (S_y - (b * S_lnx)) / n
            
            self._cache_log[1] = [a, b]
        a, b = self._cache_log[1]
        return lambda x: a + b * np.log(x - self.p_vasymp)
    def predict(self, point): 
        out = self.get_log()(point)
        self[point] = out
        return out

class p_PowerFit(Predictor): 
    def __init__(self, data, series, start = 0): 
        Predictor.__init__(self, data, series, start)
        self.p_epsilon = (max(self.series.values()) - 
                          min(self.series.values())) / 1000 # Good buffer? 
        self.p_0x = min(self.series.keys()) - 1 # Good default? 
        self.p_0y = min(self.series.values()) - self.p_epsilon
        
        self._cache_power = [None, None, None] # p_0x, p_0y, params
    def get_power(self): 
        if (self._cache_power[0] != self.p_0x or 
            self._cache_power[1] != self.p_0y): 
            self._cache_power = [self.p_0x, self.p_0y, None]
            
            xs, ys = self.series.toAxes()
            xs = [i - self.p_0x for i in xs]
            ys = [i - self.p_0y for i in ys]
            
            lnxs = [np.log(i) for i in xs]
            lnys = [np.log(i) for i in ys]
            
            S_lnx_lny = 0
            S_lnx = 0
            S_lny = 0
            S_lnx2 = 0
            for (lnx, lny) in zip(lnxs, lnys): 
                S_lnx_lny += lnx * lny
                S_lnx += lnx
                S_lny += lny
                S_lnx2 += lnx ** 2
            
            n = len(xs)
            b = ((n * S_lnx_lny) - (S_lnx * S_lny)) / ((n * S_lnx2) - 
                                                       (S_lnx) ** 2)
            a = (S_lny - (b * S_lnx)) / n
            
            self._cache_power[2] = [a, b]
        a, b = self._cache_power[2]
        return lambda x: np.exp(a) * ((x - self.p_0x) ** b) + self.p_0y
    def predict(self, point): 
        out = self.get_power()(point)
        self[point] = out
        return out

# class p_LogisticMap(Predictor): 
#     def __init__(self, data, series, start = 0): 
#         Predictor.__init__(self, data, series, start)
#         self.p_max = max(self.series.values())
#         self.p_min = min(self.series.values())
#         self.p_epsilon = (self.p_max - self.p_min) / 1000 # Good buffer? 
#         self.p_max += self.p_epsilon
#         self.p_min -= self.p_epsilon

# class p_CurveFit(Predictor): # scpop.curve_fit throws tantrums. 
#     def __init__(self, series): 
#         Predictor.__init__(self, series = series)
#         self.curve = lambda t, a, b: a * np.exp(b * t) # Exp is default. 
#         self.init_guesses = (1, 1) # (a0, b0)
        
#         self._cache_curve = (lambda: None, None) # (curve, params)
#     def get_curve(self): 
#         if (self._cache_curve[0].__code__.co_code != 
#             self.curve.__code__.co_code): # Cool way to compare functions. 
#             x = np.array(self.series.toAxes()[0])
#             y = np.array(self.series.toAxes()[1])
#             self._cache_curve = (self.curve, 
#                                  scpop.curve_fit(self.curve, x, y, 
#                                                  p0 = self.init_guesses)[0])
#         return lambda x: self.curve(x, *self._cache_curve[1])
#     def predict(self, point): 
#         out = self.get_curve()(point)
#         self[point] = out
#         return out
