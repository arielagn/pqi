import time
import serial
import RPi.GPIO as GPIO

class pqi:
    """ Clase para la comunicacion con placa de medicion
    """
    def __init__(self,pin_direcc):
        """ Funcion para inicializacion
        pin_direcc: Pin asignado a cambiar in out en RS-485 (12 para prototipo)
        """
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD) #los io son los numeros de los pines
        self.pin_direcc=pin_direcc
        GPIO.setup(pin_direcc, GPIO.OUT, initial=GPIO.HIGH)
        self.serComm=serial.Serial(
            port='/dev/ttyAMA0',
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
        self.serComm.flushInput()
        self.serComm.flushOutput()
        self.calV=162/9900*231/238
        self.calI=1/1439.255
        self.calNorm=1/32768
        
    def setW(self):
        GPIO.setup(self.pin_direcc, GPIO.OUT, initial=GPIO.HIGH)
    def resW(self):
        GPIO.setup(self.pin_direcc, GPIO.OUT, initial=GPIO.LOW)
    def compute_xor(self,vec):
        if (not vec):
            return 0
        else:
            out=0
            for i in vec:
                out = out^i
            return out
        
    def str2id(self,com):
        if (com=='reset'):
            id=0
        elif (com=='setFs'):
            id=1
        elif (com=='getVI'):
            id=2
        elif (com=='sendV'):
            id=3
        elif (com=='sendI'):
            id=4
        elif (com=='seekV'):
            id=5
        elif (com=='seekI'):
            id=6
        elif (com=='tellV'):
            id=7
        elif (com=='tellI'):
            id=8
        elif (com=='lenV'):
            id=9
        elif (com=='lenI'):
            id=10
        elif (com=='busy'):
            id=11
        elif (com=='testRam'):
            id=12
        elif (com=='getNormVI'):
            id=13
        else:
            id=255
        return id
        
    def sendCom(self,com,arg):
        """ Funcion para enviar comando al pqi
        input:
            com: string con el comando
            arg: valor segun comando
        """
        self.serComm.flushInput()
        self.serComm.flushOutput()
        comId=self.str2id(com)
        sender = comId.to_bytes(1,'little')
        self.setW()
        if (arg==8000000):
            sender = [12,12]
        else:
            sender += arg.to_bytes(4,'little')
            xorResult = self.compute_xor(sender)
            sender += xorResult.to_bytes(1,'little')
        self.serComm.write(sender)
        #print(sender)
        time.sleep(0.02)
        self.resW()
        data=b''
        rxTrue=True
        readTimer=time.time()
        while (rxTrue):
            if (self.serComm.in_waiting > 0):
                data+=self.serComm.read(self.serComm.in_waiting)
                readTimer=time.time()
            else:
                diffTime=time.time()-readTimer
                if (diffTime>=1):
                    rxTrue=False
        num=[]
        if (data==b''):
            return 'no responce'
        xorResult=self.compute_xor(data)
        if (xorResult==0):
            for i in range(2,len(data)-1,2):
                num.append(data[i]*256+data[i+1]-32768)      #int.from_bytes(data[i:i+1],"little")-pow(2,15))
            return num
        else:
            return 'fail xor'
        
        """
        
        num=[]
for i in range(1,len(d),2):
	num.append(int.from_bytes(d[i:i+1],"big"))
        
        
        
        try:
            data+=self.serComm.read(2400)
        except serial.SerialException as e:
            print(e)
        while (rxTrue):
            if (self.serComm.in_waiting > 0):
                data+=self.serComm.read(self.serComm.in_waiting)
                readTimer=time.time()
            else:
                diffTime=time.time()-readTimer
                if (diffTime>=1):
                    rxTrue=False
        """
        return data
    
        
            
        
        
                
            
            
        
