import numpy as np
from abc import abstractmethod, ABCMeta

class HasProperties(metaclass = ABCMeta): 
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
        # print(str(data[:20]))
        data -= np.mean([i for i in data if i != None])
        # amp = 3*np.std(data)/(2**0.5)
        # data /= amp
        return len(self.toList()) / np.argmax(np.absolute(np.fft.rfft(data)))
    
    @use_hint('deg')
    def get_deg(self): 
        return 3 # TODO?
    
    @use_hint('tone')
    def get_tone(self): 
        first = self[min(self.keys())]
        last = self[max(self.keys())]
        if last >= first: 
            return 1
        else: 
            return -1
