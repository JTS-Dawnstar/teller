### UNUSED ###

from .datatypes import TimeList, TimeSeries

def moving_average(series, domain = range(-5, 5)): 
    if isinstance(series, (TimeList, list)): 
        try: 
            y = series.toAxes()[1]
            start = series.start
        except AttributeError: 
            y = series
            start = 0
        out = [0] * len(y)
        for i in range(len(y)): 
            to_avg = []
            for disp in domain: 
                try: 
                    to_avg.append(series[i + disp])
                except (IndexError, KeyError): 
                    pass
            out[i] = sum(to_avg) / len(to_avg)
        return TimeList(out, start = start)
    elif isinstance(series, TimeSeries): 
        return TimeSeries([moving_average(table) for table in series.tables])
