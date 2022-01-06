import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD) #los io son los pines
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Canal del anemometro

class anemometro():
    def __init__(self):  # intervalo de muestras en 60 segundos
        self.count=0
        self.val=[]
        self.sts=0
        GPIO.add_event_detect(16, GPIO.RISING, callback=self.rising_callback)  # add rising edge detection on a channel
        

    def parcial(self,diferencia):
        self.val.append(0.765 * (self.count/diferencia) + 0.35)
        #print(diferencia)
        self.count = 0
        if (len(self.val)>=60):
            self.sts=2
        
      
    def rising_callback(self,anechannel):
        if (anechannel==16 and self.sts==1):
            self.count += 1

    def start(self):
        tini=time.time()
        self.sts=1
        while (self.sts==1):
            actual=time.time()
            diferencia=actual-tini
            if (diferencia>=1):
                self.parcial(diferencia)
                tini=time.time()
        minimo=100
        maximo=0
        promedio=0
        contador=0
        suma=0
        for i in self.val:
            if (i>=maximo):
                maximo=i
            if (i<=minimo):
                minimo=i
            suma=suma+i
            contador=contador+1
        promedio=suma/contador
        return promedio,maximo,minimo
        
            

