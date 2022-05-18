from scipy import signal
import sys
import numpy as np
import time
import pqi
#import anemometro
import anedig2
import flicker
import psycopg2
from test_dbconn import config

res=float(sys.argv[1])
ind=float(sys.argv[2])
sn = float(sys.argv[3])
skfic=(220 ** 2)/(np.sqrt(res**2+(2*np.pi*50*ind)**2))
rcc=skfic/sn
ang=180/np.pi*np.arctan(2*np.pi*50*ind/res)
#print( rcc ,ang)


s=pqi.pqi(12)
s.setW()
#ane=anemometro.anemometro()
ane=anedig2.aneDig(60)

# muestreo FS=31507Hz prescalar p FS*=FS/(p+1)
# p=15 FS*=1969,2Hz
# p=5  FS*=5251,2Hz
# p=0  FS*=31507Hz
d=s.sendCom('setFs',15) #seteo muestro a 1969,2
#print(d)

d=s.sendCom('getNormVI',144000)
#print(d) #sacar
time.sleep(12)
stamp=time.strftime("\"%Y-%m-%d %H:%M:%S\"")

viprom,vimediana,vistd=ane.start()
#viprom=1
#vimediana=1
#vistd=1
time.sleep(65)
#print("traerV") #sacar
u=s.sendCom('sendV',144000)
#print(len(u)) #sacar
uarr=np.array(u)
ucal=uarr*s.calNorm*311.127


#print("traerI") #sacar
i=s.sendCom('sendI',144000)
iarr=np.array(i)
ical=iarr*s.calI
#print(len(i))

f=flicker.flicker(2000,50,220)

uo=f.Vficticia(res,ind,ucal,ical )
uoNorm = f.normSignalWoFil(uo)
z = f.filters(uoNorm)
ps,perc,pst = f.flicker(z[24000:],65)
_,vrms = f.rms(uo)
_,irms = f.rms(ical)



#if (pst>1):
#    np.savetxt(stamp+".csv",z,delimiter=",")
print("{\"time\":",stamp,", \"vprom\":",viprom,", \"vmediana\":",vimediana,", \"vstd\":",vistd,", \"pst\":",pst,", \"vrms\":",vrms,", \"irms\":",irms,", \"rcc\":",rcc,", \"ang\":",ang,"}")

sql = ("INSERT INTO flicker(tiempo,vprom,vmediana,vstd,pst,"
        "vrms,irms,rcc,ang) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)")
conn = None

try:
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    cur.execute(sql,(stamp,viprom,vimediana,vistd,
                     pst,vrms,irms,rcc,ang))
    conn.commit()
    cur.close()
except (Ecveption,psycopg2.DatabaseError) as error:
    print (error)
finally:
    if conn is not None:
        conn.close()







