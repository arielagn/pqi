
import serial
import numpy as np
import matplotlib.pyplot as plt
import struct


class pqi_serial:
    def __init__(self,com) -> None:
        self.serComm=serial.Serial(
            port=com,
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )

#ser=serial.Serial('com5',9600, timeout=1)
    def pqi_v_offset(self,val):
         self.serComm.write(b'g'+bytearray(struct.pack("<f",val)))
         #self.serComm.write()
         return
    def pqi_v_scale(self,val):
         self.serComm.write(b'h'+bytearray(struct.pack("<f",val)))
         #self.serComm.write()
         return
    def pqi_i_offset(self,val):
         self.serComm.write(b'i'+bytearray(struct.pack("<f",val)))
         #self.serComm.write()
         return
    def pqi_i_scale(self,val):
         self.serComm.write(b'j'+bytearray(struct.pack("<f",val)))
         #self.serComm.write()
         return
    
    def pqi_cal(self,n):
        if (n==1):
             self.serComm.write(b't1')     # write a string
        elif (n==2):
             self.serComm.write(b't2')     # write a string
        else:
             return 

        #self.serComm.write(b'c')     # write a string
        s=b''
        while (s==b''):
            s=self.serComm.read(16);
        f=np.frombuffer(s,dtype="float32")

        print('V RMS:'+str(f[0]))
        print('V DC:'+str(f[1]))
        print('I RMS:'+str(f[2]))
        print('I DC:'+str(f[3]))
        #self.serComm.close()             # close port
        return

    def pqi_medicion(self, n):
        if (n==1):
             self.serComm.write(b't1')     # write a string
        elif (n==2):
             self.serComm.write(b't2')     # write a string
        else:
             return 

        s=b''
        while (s==b''):
            s=self.serComm.read(3200);
        f=np.frombuffer(s,dtype="float32")
        print(len(f))
        print('V RMS:'+str(f[0]))
        print('V DC:'+str(f[1]))
        print('I RMS:'+str(f[2]))
        print('I DC:'+str(f[3]))
        # Initialise the subplot function using number of rows and columns
        figure, axis = plt.subplots(2, 1)
        # For tension
        axis[0].plot(f[4:401])
        axis[0].set_title("Tension")
        # For current
        axis[1].plot(f[402:799])
        axis[1].set_title("Corriente")
        plt.grid()
        plt.show()
        #self.serComm.close()             # close port
        return
    def pqi_fft(self,n):
            if (n==1):
                self.serComm.write(b'f1')     # write a string
            elif (n==2):
                self.serComm.write(b'f2')     # write a string
            else:
                return 
           
            s=b''
            while (s==b''):
                s=self.serComm.read(636);
            f=np.frombuffer(s,dtype="float32")
            print(len(f))
            print('I DC por FFT:'+str(f[150]))
            print('P Aparente:'+str(f[151]))
            print('P Activa:'+str(f[152]))
            print('P Reactiva:'+str(f[153]))
            print('THC:'+str(f[154]))
            print('V RMS por t:'+str(f[155]))
            print('V DC por t:'+str(f[156]))
            print('I RMS por t:'+str(f[157]))
            print('I DC por t:'+str(f[158]))
            # create plot
            figure, axis = plt.subplots(2, 1)
            index = np.arange(1,50) # numero de barras 1 por armonico
            bar_width = 0.35
            opacity = 0.8

            axis[0].bar(index, f[0:49], bar_width,
            alpha=opacity,
            color='b',
            label='Armonicos V')
            axis[0].legend()

            axis[1].bar(index + bar_width, f[50:99], bar_width,
            alpha=opacity,
            color='g',
            label='Armonicos I')
            axis[1].legend()
            """
            axis[1] = plt.bar(index + bar_width, f[100:149], bar_width,
            alpha=opacity,
            color='r',
            label='Sub Armonicos I')
            """
            plt.xlabel('Armonico - Grupo')
            plt.ylabel('Amplitud')
            plt.title('Armonicos')
            #plt.xticks(index + bar_width, range(50))
            plt.legend()

            plt.tight_layout()
            plt.show()
            #self.serComm.close()             # close port
            return
    def pqi_rp_fft(self):
        self.serComm.write(b'f2')     # write a string
        s=b''
        while (s==b''):
            s=self.serComm.read(636);
        f=np.frombuffer(s,dtype="float32")
        return f

"""
# create plot
            fig, ax = plt.subplots()
            index = np.arange(50) # numero de barras 1 por armonico
            bar_width = 0.35
            opacity = 0.8

            rects1 = plt.bar(index, f[0:50], bar_width,
            alpha=opacity,
            color='b',
            label='Armonicos V')

            rects2 = plt.bar(index + bar_width, f[50:100], bar_width,
            alpha=opacity,
            color='g',
            label='Armonicos I')

            rects3 = plt.bar(index + bar_width, f[100:150], bar_width,
            alpha=opacity,
            color='r',
            label='Sub Armonicos I')

            plt.xlabel('Armonico - Grupo')
            plt.ylabel('Amplitud')
            plt.title('Armonicos')
            plt.xticks(index + bar_width, range(50))
            plt.legend()

            plt.tight_layout()
            plt.show()

"""

