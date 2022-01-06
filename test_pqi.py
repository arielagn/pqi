from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import time
import pqi
import anemometro
import fliker

s=pqi.pqi(12)
s.setW()


d=s.sendCom('getVI',60000)
print(d)

            
#ane=anemometro.anemometro()
#print (ane.start())
time.sleep(33)
#print("traerV")
#d=s.sendCom('sendV',60000)


#de=np.array(d,dtype='float')

#defV=de*s.calV

#print(len(d))

print("traerI")
d=s.sendCom('sendI',60000)


de=np.array(d,dtype='float')

defI=de*s.calI

print(len(d))
"""

"""
#f=fliker.fliker(2000,50,220)
#v = f.normSignalWoFil(defV)
#_,vrms = f.rms(v)
#print("val rms",vrms)
#u,t = f.genSignal(0,18,10,True)
#d=np.append(u,defl)
#v = f.normSignal(defl)
#v = f.normSignalWoFil(defl)

#z = f.filters(v)
#np.savetxt("datos.cvs",z,delimiter=",")
#ps,perc,pst = f.fliker(z[24000:],65)
#ps2,perc2,pst2 = f.fliker(z[80000:],65)

#print("Fliker=",pst)
#print("Fliker=",pst2)
#print("percentil=",perc)
#print("frq acum=",ps[0,:])
#print("clase inf=",ps[1,:])
#print("clase sup=",ps[2,:])
#print("frq acum=",ps[3,:])
#print("len",len(ps[0,:]))



plt.xlabel('time [s]')
plt.ylabel('Amplitude [V]')
#plt.ylim(300,320)
plt.title('Tension')
#plt.plot(defV)
plt.plot(defI)
plt.grid()
plt.show()

