from scipy import signal
import numpy as np
import time
import pqi
#import anemometro
import anedig2
import fliker

s=pqi.pqi(12)
s.setW()
#ane=anemometro.anemometro()
ane=anedig2.aneDig()

d=s.sendCom('getNormVI',144000)
print(d) #sacar
time.sleep(12)
stamp=time.strftime("\"%Y-%m-%d %H:%M:%S\"")

viprom,vimax,vimin=ane.start()
time.sleep(7)
print("traerV") #sacar
u=s.sendCom('sendV',144000)
print(len(u)) #sacar
uarr=np.array(u)
ucal=uarr*s.calNorm*311.127


print("traerI") #sacar
i=s.sendCom('sendI',144000)
iarr=np.array(i)
ical=iarr*s.calI
print(len(i))

f=fliker.fliker(2000,50,220)

uo=f.Vficticia(2.383,0.001338,ucal,ical )
uoNorm = f.normSignalWoFil(uo)
z = f.filters(uoNorm)
ps,perc,pst = f.fliker(z[24000:],65)
_,vrms = f.rms(uo)
_,irms = f.rms(ical)

uo2=f.Vficticia(1.192,0.000669,ucal,ical )
uoNorm2 = f.normSignalWoFil(uo2)
z2 = f.filters(uoNorm2)
ps2,perc2,pst2 = f.fliker(z2[24000:],65)



if (pst>1):
    np.savetxt(stamp+".csv",z,delimiter=",")
print("{\"time\":",stamp,", \"vienmin\":",vimin,", \"vienmax\":",vimax,", \"vienprom\":",viprom,", \"pst\":",pst,", \"vrms\":",vrms,", \"irms\":",irms,", \"pst2\":",pst2,"}")

"""

"""


