import os
from .datatypes import TimeList, TimeSeries

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
