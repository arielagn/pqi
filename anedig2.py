import time
import serial
import re
import numpy as np

class aneDig():
    def __init__(self,duracion):
        self.duracion=duracion
        self.sts=0
        self.count=0
        self.val=[]
        self.serComm=serial.Serial(
            port='/dev/ttyUSB0',
            baudrate=38400,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
        self.serComm.flushInput()
        self.serComm.flushOutput()
        
    def resd(self):
        rxtrue=True
        data=b''
        while (rxtrue):
            data=self.serComm.read(1)
            #print (data) #sacar
            if (data==b'$'):
                data=self.serComm.read(27)
                rxtrue=False
        
        return data

    def deco(self,data):
        #data='UUU$06453.06751.0899.01143.111.3bfd*QQQ'
        pattern = '\.'
        sep=re.split(pattern,data.decode('utf-8'))
        #freq = int(sep[3])/10
        #freq=1510
        vel =0.04597*int(sep[3])/10+0.2156
        #temp=55.342*int(sep[0])-86.154
        #dire=1.008*int(sep[2])+6
        #pres=217.9*int(sep[1])+103.4
        #vel =int(sep[0])
        #temp=int(sep[1])
        #dire=int(sep[2])
        #pres=int(sep[3])
        return vel
    
    
            
    def start(self):
        tini=time.time()
        self.sts=1
        while (self.sts==1):
            actual=time.time()
            diferencia=actual-tini
            data=self.resd()
            vel=self.deco(data)
            #print(vel)
            self.val.append(vel)
            if (diferencia>=self.duracion):
                self.sts=2
        promedio=np.mean(self.val)
        media=np.median(self.val)
        estand=np.std(self.val)
        return promedio,media,estand
        
