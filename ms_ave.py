# averaging ms
from pyrap.tables import table
import numpy as np
t = table('MeerKATlores.MS_p0_p0',readonly=False)
data = t.getcol('DATA')
A1 = t.getcol('ANTENNA1')
A2= t.getcol('ANTENNA2')
average = (np.zeros_like(data))
na = np.max(A1)+1
for p in range(na):
    for q in range(p+1, na):
        datauv = data[(A1==p)&(A2==q)]
        ave_data = np.mean(datauv,axis=0)
        average[(A1==p)&(A2==q)] = ave_data

ave_data = data
t.putcol('CORRECTED_DATA')
t.putcol('DATA',average)
t.close()

