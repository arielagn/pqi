from scipy import fft #,fftfreq #fftpack #,fttfreq,rfft
from scipy.fftpack import fftfreq
from scipy.signal import find_peaks
import numpy as np
import pqi
import matplotlib.pyplot as plt
import time

s=pqi.pqi(12)
s.setW()
#cantidad de muestras
N=6302
# muestreo FS=31507Hz prescalar p FS*=FS/(p+1)
# p=15 FS*=1969,2Hz
# p=5  FS*=5251,2Hz
# p=0  FS*=31507Hz
fs=31507
d=s.sendCom('setFs',0)
print(d)

d=s.sendCom('getVI',N)
print(d) #sacar
time.sleep(2)

print("traerV") #sacar
u=s.sendCom('sendV',N)
print(len(u)) #sacar
uarr=np.array(u)
ucal=uarr*s.calV

print("traerI") #sacar
i=s.sendCom('sendI',N)
print(len(i)) #sacar
iarr=np.array(i)
ical=iarr*s.calI
# fft
ucalf=fft(ucal)[0:N//2]  #fftpack.fft(ucal)
f=fftfreq(N,1/fs)[0:N//2]
icalf=fft(ical)
# deteccion de picos
espect=np.zeros(len(ucalf))
espect=2.0/N*np.abs(ucalf)
    
print(len(espect))
peaks, _ = find_peaks(espect, height=0.2)


plt.xlabel('freq [Hz]')
plt.ylabel('Amplitude [V]')
plt.title('Tension')
plt.plot(f,espect)
plt.plot(f[peaks], espect[peaks], "x")
plt.grid()
plt.show()
