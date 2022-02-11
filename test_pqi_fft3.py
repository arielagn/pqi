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
ucalf=fft(ucal)[0:(N//2)-1]*2.0/N #fftpack.fft(ucal)
ucalfNoDc=ucalf[1:(N//2)-1]
f=fftfreq(N,1/fs)[0:(N//2)-1]
icalf=fft(ical)[0:(N//2)-1]*2.0/N
icalfNoDc=icalf[1:(N//2)-1]
icalf[0]=icalf[0]/2
# Calculo de valores RMS
UPowerEspec=(ucalfNoDc.real**2)+(ucalfNoDc.imag**2)
Urms=np.sqrt(np.sum(UPowerEspec)/2.0)
IPowerEspec=icalf.real**2+icalf.imag**2
Irms=np.sqrt(np.sum(IPowerEspec)/2.0)
# DC corriente
IDc=np.abs(icalf[0])
# Potencias activa, reactiva, aparente, factor de potenca
PAct=np.sum(icalfNoDc.real*ucalfNoDc.real+icalfNoDc.imag*ucalfNoDc.imag)/2.0
PRea=np.sum(icalfNoDc.real*ucalfNoDc.imag-icalfNoDc.imag*ucalfNoDc.real)/2.0
PApar=Urms*Irms
PowerFactor=PAct/PApar


print("U rms="+str(Urms))
print("I rms="+str(Irms))
print("I dc="+str(IDc))
print("Pot Act="+str(PAct))
print("Pot Reac="+str(PRea))
print("Fact Pot="+str(PowerFactor))
print("Pot Apare="+str(PApar))

"""
espect=np.zeros(len(ucalf))
espect=2.0/N*np.abs(ucalf)
    
print(len(espect))
peaks, _ = find_peaks(espect, height=0.2)
"""

plt.xlabel('time')
plt.ylabel('Amplitude [V]')
plt.title('Tension')
plt.plot(ucal)

plt.grid()
plt.show()

