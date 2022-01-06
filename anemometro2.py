import time
import RPi.GPIO as GPIO
from threading import Timer,Thread,Event
GPIO.setmode(GPIO.BCM) #los io son los canales
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Canal del anemometro

class anemometro():
    def __init__(self,t):  # t intervalo de muestras en segundos
        self.t=t
        self.count=0
        self.val=0
        GPIO.add_event_detect(4, GPIO.RISING, callback=self.rising_callback)  # add rising edge detection on a channel
        self.thread = Timer(self.t,self.handle_function)

    def handle_function(self):
        self.val = 0.765 * (self.count/self.t) + 0.35
        print ("val=",self.val)
        self.count = 0
        self.thread = Timer(self.t,self.handle_function)
        self.thread.start()
      
    def rising_callback(self,anechannel):
        if (anechannel==4):
            self.count += 1

    def start(self):
        self.thread.start()

    def cancel(self):
        self.thread.cancel()
        GPIO.remove_event_detect(4)

ane=anemometro(10)
ane.start()

while (True):
    print("--")
    time.sleep(2)








    ane.cancel