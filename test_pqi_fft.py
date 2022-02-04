from scipy import fft #,fftfreq #fftpack #,fttfreq,rfft
from scipy.fftpack import fftfreq
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
ucalf=fft(ucal)  #fftpack.fft(ucal)
f=fftfreq(N,1/fs) # fftpack.fftfreq(N,1/fs) #[0:N//2] [0:N//2]
icalf=fft(ical)

figure, axis=plt.subplots(2,2)
axis[0,0].set_title("Tension")
axis[0,0].plot(ucal)

axis[0,1].set_title("Corriente")
axis[0,1].plot(ical)

axis[1,0].set_title("Tension FFT")
axis[1,0].plot(f,2.0/N*np.abs(ucalf))

axis[1,1].set_title("Corriente FFT")
axis[1,1].plot(f,2.0/N*np.abs(icalf))

plt.show()
"""
plt.xlabel('time [s]')
plt.ylabel('Amplitude [V]')
plt.title('Tension')
plt.plot(ucal)
plt.grid()
plt.show()

plt2.xlabel('time [s]')
plt2.ylabel('Amplitude [I]')
plt2.title('Corriente')
plt2.plot(ical)
plt2.grid()
plt2.show()

ucalf=fftpack.fft(ucal)
f=fftpack.fftfreq(N,1/fs) #[0:N//2]
#fr=fftpack.fftshift(f)
#print(len(ucalf))
#print(len(f))
#print(f[6000:6100])

plt3.xlabel('freq [Hz]')
plt3.ylabel('Amplitude [V]')
plt3.title('Tension')
plt3.plot(f[0:600],2.0/N*np.abs(ucalf)[0:600])
plt3.grid()
plt3.show()
"""