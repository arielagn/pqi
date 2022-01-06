from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import time
import pqi
import anemometro
import fliker

s=pqi.pqi(12)
s.setW()


d=s.sendCom('getNormVI',144000)
print(d)

            
#ane=anemometro.anemometro()
#print (ane.start())
time.sleep(80)
print("traerV")
u=s.sendCom('sendV',144000)
u=np.array(u)
ucal=u*s.calNorm*311.127
print(len(u))
print("traerI")
i=s.sendCom('sendI',144000)
i=np.array(i)
ical=i*s.calI
print(len(i))

f=fliker.fliker(2000,50,220)
_,vrms = f.rms(ucal)
print("val rms",vrms)
uo=f.Vficticia(1.048,0.001926,ucal,ical )

uoNorm = f.normSignalWoFil(uo)

z = f.filters(uoNorm)
ps,perc,pst = f.fliker(z[24000:],65)
print (" PST =",pst)
"""

"""





plt.xlabel('time [s]')
plt.ylabel('Amplitude [V]')
#plt.ylim(300,320)
plt.title('Tension Ficticia')
plt.plot(ucal)
plt.plot(uo)
plt.grid()
plt.show()

