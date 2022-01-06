import time
import RPi.GPIO as GPIO
import dht11
from threading import Timer,Thread,Event
from paho.mqtt import client as mqtt_client
#broker = '192.168.0.104'
#port = 1883
#topic = "/depto/sensores"



class raspSensores():
    def __init__(self,t,pin_anemo,pin_dht,broker,port,topic):
        """
        Constructor de la clase
        inputs:
        t intervalo de muestras en segundos
        pin_anemo pin donde esta conectado el anemometro
        pin_dht pin donde esta conectado el sensor de temp y humedad
        broker direccion del broker mqtt
        port port del broker
        topic potic to publish
        """
        self.t=t
        self.pin_anemo=pin_anemo
        self.pin_dht=pin_dht
        self.broker=broker
        self.port=port
        self.topic=topic
        # initialize GPIO
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.cleanup()
        GPIO.setup(self.pin_anemo, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Canal del anemometro
        # read data using pin 14
        self.instance = dht11.DHT11(pin = self.pin_dht)
        self.instance.read()
        self.count=0
        self.vel=0
        self.temp=0
        self.hume=0
        self.timeStart=time.time() # al correr el constructor tomo la primera estampa
        GPIO.add_event_detect(self.pin_anemo, GPIO.RISING, callback=self.rising_callback)  # add rising edge detection on a channel
        # generate client ID with pub prefix randomly
        self.client_id = 'python-mqtt-rasp'
        # username = 'emqx'
        # password = 'public'


    def rising_callback(self,anechannel):
        if (anechannel==4):
            self.count += 1

    def sensoresTask(self):
        timeNow=time.time()
        if (timeNow-self.timeStart>=self.t):
            result = self.instance.read()
            if result.is_valid():
                self.temp = result.temperature
                self.hume = result.humidity
            else:
                print("Error: %d" % result.error_code)
#                 self.temp = 0
#                self.hume = 0
            self.vel = 0.765 * (self.count/(timeNow-self.timeStart)) + 0.35
            msg = f'{{ \"temp\":{self.temp},\"hume\":{self.hume},\"vel\":{self.vel},\"DT\":{timeNow-self.timeStart} }}'
            self.connect_mqtt(msg)
            self.count = 0
            self.timeStart=timeNow
            
    def connect_mqtt(self,msg):
        def on_connect(client,userdata,flags,rc):
            if rc==0:
                print("connected OK returned code=",rc)
            else:
                print("Bad connection returned code=",rc)
                    
        client = mqtt_client.Client(self.client_id)
        # client.username_pw_set(username, password)
        client.on_connect = on_connect
        client.connect(self.broker, self.port)
        result = client.publish(self.topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{self.topic}`")
        else:
            print(f"Failed to send message to topic {self.topic}")
               

def run():
    sen=raspSensores(10,4,2,'192.168.0.116',1883,"/depto/sensores")
    while True:
        sen.sensoresTask()


if __name__ == '__main__':
    run()


