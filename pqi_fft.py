from scipy import fft #,fftfreq #fftpack #,fttfreq,rfft
from scipy.fftpack import fftfreq
from scipy.signal import find_peaks
import numpy as np
import pqi
# import matplotlib.pyplot as plt
import time
import anedig2
import psycopg2
from test_dbconn import config

s=pqi.pqi(12)
s.setW()
ane=anedig2.aneDig(3)

# muestreo FS=31507Hz prescalar p FS*=FS/(p+1)
# p=15 FS*=1969,2Hz
# p=5  FS*=5251,2Hz
# p=0  FS*=31507Hz
# Con esto cumplo con la armonica 50
# 50x50=2500Hz
fs=5251 #31507
#cantidad de muestras
# Para N=1050 tengo 10 ciclos completos
# para N=15754 tengo 3sg. que son 15 series de 0,2sg (10 ciclos)
series=15
ventana=1050
N=series*ventana #15754 
d=s.sendCom('setFs',5) #0)
#print(d)


d=s.sendCom('getVI',N)
#print(d) #sacar

stamp=time.strftime("\"%Y-%m-%d %H:%M:%S\"")
viprom,vimediana,vistd=ane.start()
#viprom=1
#vimediana=1
#vistd=1

time.sleep(4)

#print("traerV") #sacar
u=s.sendCom('sendV',N)
#print(len(u)) #sacar
uarr=np.array(u)
ucal=uarr*s.calV

#print("traerI") #sacar
i=s.sendCom('sendI',N)
#print(len(i)) #sacar
iarr=np.array(i)
ical=iarr*s.calI
# frequency array
f=fftfreq(ventana,1/fs)[0:(ventana//2)-1]

#  FFT
freq=np.zeros(series)
Urms=np.zeros(series)
Irms=np.zeros(series)
THD_U=np.zeros(series)
THD_I=np.zeros(series)
I_dc=np.zeros(series)
P=np.zeros(series)
Q=np.zeros(series)
S=np.zeros(series)
PF=np.zeros(series)
Pdesf=np.zeros(series)
UrmsPoli=np.zeros(series)
IrmsPoli=np.zeros(series)
for i in range(series):
    ucalf=fft(ucal[i:i+ventana])[0:(ventana//2)-1]*2.0/ventana/np.sqrt(2)
    icalf=fft(ical[i:i+ventana])[0:(ventana//2)-1]*2.0/ventana/np.sqrt(2)
    ucalf_abs=np.abs(ucalf)
    icalf_abs=np.abs(icalf)
    # Deteccion de pico fundamental
    # este Unom e Inom puede ser ingrsado o lo saco de la mediocion
    Unom=np.max(ucalf_abs)
#     Inom=np.max(np.abs(icalf))
    Uhumbral=Unom*0.001 ## umbral 0,1% Unom
#     Ihumbral=Inom*0.001
    peaks, _ = find_peaks(ucalf_abs, height=Uhumbral)
#     ipeaks, _ = find_peaks(icalf_max, height=Ihumbral)
    #  DC corriente
    I_dc[i]=icalf_abs[0]*2.0
#     Feq
    freq[i] = f[peaks[0]]
    Urms[i] = ucalf_abs[peaks[0]]
    Irms[i] = icalf_abs[peaks[0]]
    UrmsPoli[i] =np.sqrt(np.sum(ucalf_abs[peaks]**2))
    IrmsPoli[i] =np.sqrt(np.sum(icalf_abs[peaks]**2)+I_dc[i]**2)
    #  Calculo de distorsion armonica general
    THD_U[i]=np.sqrt(np.sum((ucalf_abs[peaks[1:]]/ucalf_abs[peaks[0]])**2))*100
    THD_I[i]=np.sqrt(np.sum((icalf_abs[peaks[1:]]/icalf_abs[peaks[0]])**2))*100
   
    # Potencia calculado solo con la armonica principal
    P[i]=ucalf[peaks[0]].real*icalf[peaks[0]].real+ucalf[peaks[0]].imag*icalf[peaks[0]].imag
    Q[i]=ucalf[peaks[0]].imag*icalf[peaks[0]].real-ucalf[peaks[0]].real*icalf[peaks[0]].imag
    S[i]=Urms[i]*Irms[i]
    PF[i]=P[i]/S[i]
    # potencia de desformacion (con la hipotesis de THDi e THDu menor a 5% 
    Pdesf[i]= Urms[i]*np.sqrt(np.sum(icalf_abs**2)-icalf_abs[0]**2)

sql = ("INSERT INTO power(tiempo,vprom,vmediana,vstd,freq,"
        "urms,irms,urmspoli,irmspoli,thdu,thdi,idc,pact,preac,"
        "papar,factpot,pdesf) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,"
        "%s,%s,%s,%s,%s,%s,%s,%s)")
conn = None

freq_av=np.average(freq)
Urms_av=np.average(Urms)
Irms_av=np.average(Irms)
UrmsPoli_av=np.average(UrmsPoli)
IrmsPoli_av=np.average(IrmsPoli)
THD_U_av=np.average(THD_U)
THD_I_av=np.average(THD_I)
I_dc_av=np.average(I_dc)
P_av=np.average(P)
Q_av=np.average(Q)
S_av=np.average(S)
PF_av=np.average(PF)
Pdesf_av=np.average(Pdesf)
if (freq_av>49):
    print("{\"time\":",stamp,", \"vprom\":",viprom,", \"vmediana\":",vimediana,", \"vstd\":",vistd,", \"freq\":",freq_av,
      ", \"Urms\":",Urms_av,
      ", \"Irms\":",Irms_av,
      ", \"UrmsPoli\":",UrmsPoli_av,
      ", \"IrmsPoli\":",IrmsPoli_av,
      ", \"THDu\":",THD_U_av,
      ", \"THDi\":",THD_I_av,
      ", \"IDC\":",I_dc_av,
      ", \"Pact\":",P_av,
      ", \"Preac\":",Q_av,
      ", \"Papar\":",S_av,
      ", \"FactPot\":",PF_av,
      ", \"Pdesf\":",Pdesf_av,
      "}")
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql,(stamp,viprom,vimediana,vistd,
                         freq_av,Urms_av,Irms_av,UrmsPoli_av,IrmsPoli_av,
                         THD_U_av,THD_I_av,I_dc_av,P_av,Q_av,S_av,
                         PF_av,Pdesf_av))
        conn.commit()
        cur.close()
    except (Ecveption,psycopg2.DatabaseError) as error:
        print (error)
    finally:
        if conn is not None:
            conn.close()

    
