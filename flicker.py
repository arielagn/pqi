from scipy import signal
import numpy as np
import matplotlib.pyplot as plt

class flicker:
    """Clase para calculo de flicker"""
    def __init__(self,fs,line_freq,U_nom):
        """ Funcion para inicializacion
        fs: frecuencia de muestreo
        line_freq: 50 para 50Hz o 60 para 60Hz
        U_nom: Tension rms nominal
        """
        self.fs = fs
        self.U_nom = U_nom
        self.line_freq = line_freq
        'Voltage adaptor low pass filter 27,3s'
        num=[1]
        den=[27.3,1]
        lti=signal.lti(num,den)
        self.z1,self.p1=signal.bilinear(lti.num,lti.den,self.fs)
        'Weighting filter block3 1st order HP 6th order LP'
        tc = 1/ (2 * np.pi * 0.05)
        num=[tc,0]
        den=[tc,1]
        #lti2=signal.lti(num,den)
        # Pasa bajo
        if (line_freq==60):
            wn =2*np.pi* 42
        else:
            wn =2*np.pi* 35
        b, a = signal.iirfilter(6,wn , rp=None, rs=None, btype='lowpass', analog=True, ftype='butter', output='ba')
        #lti3=signal.lti(b,a)
        # Combinando los filtros
        lti4=signal.lti(np.polymul(b,num),np.polymul(a,den))
        #Digitalizacion
        self.z2,self.p2=signal.bilinear(lti4.num,lti4.den,self.fs)
        'Weighting filter block3'
        if (line_freq==60):
            k=1.6357 #1.74802
            lamda=2*np.pi*4.167375 #4.05981
            omega1=2*np.pi*9.077169 #9.15494
            omega2=2*np.pi*2.939902 #2.27979
            omega3=2*np.pi*1.394468 #1.22535
            omega4=2*np.pi*17.31512 #21.9
        else:
            k=1.74802
            lamda=2*np.pi*4.05981
            omega1=2*np.pi*9.15494
            omega2=2*np.pi*2.27979
            omega3=2*np.pi*1.22535
            omega4=2*np.pi*21.9
        num1=[k*omega1,0]
        den1=[1,2*lamda,omega1**2]
        num2=[1/omega2,1]
        den2=[1/omega3,1]
        den3=[1/omega4,1]
        den4=np.polymul(den2,den3)
        num5=np.polymul(num1,num2)
        den5=np.polymul(den1,den4)
        lti5=signal.lti(num5,den5)
        #Digitalizacion
        self.z3,self.p3=signal.bilinear(lti5.num,lti5.den,self.fs)
        'Pasa bajos de 1er orden 0.3s de constante de tiempoo'
        # frecuencia de corte 0,53Hz w=3.33
        num=[1]
        den=[0.3,1]
        lti=signal.lti(num,den)
        self.z4,self.p4=signal.bilinear(lti.num,lti.den,self.fs)

    def genSignal(self,du_u,ff,tl,square):
        """
        Funcion para generar señal de prueba 
        inputs
        du_u = 0.196   #input relative voltage fluctuation delta U/U [%]
        ff   = 8.8     #frecuencia de flucuacion [Hz]
        tl   = 1       #Longitud en tiempo [s]
        square true    #Modulada cuadrada
        return 
        vector de señal 
        """
        up = self.U_nom * np.sqrt(2)
        t    = np.arange(0,tl,1/self.fs)
        if (square):
            u    = up * np.sin( 2* np.pi * self.line_freq *t) * (1+0.5* du_u  /100 * np.sign(np.sin(2*np.pi*ff*t)))
        else:
            u    = up * np.sin( 2* np.pi * self.line_freq *t) * (1+0.5* du_u  /100 * np.sin(2*np.pi*ff*t))
        return u,t

    
    def rms(self,vector):
        """
        Funcion para calculo de valor rms. 
        Retorna un vector con valores rms calculados en un periodo 1/ft. 
        El vector retornado tiene la dimension del vector de entrada, durante el periodo se repite el
        valor rms
        Para el primer período se asume valor inicial ingresado. 
        :Param vector: vector con valores de tension
        :Return: vector con valores rms 
        :Return: rms of array
        """
        k=0
        sum=0
        vrms=self.U_nom
        sal = []
        muestras=self.fs/(2*self.line_freq)
        for i in vector:
            if k<muestras:
                sum=sum+i**2
                k=k+1
            else:
                vrms=np.sqrt(sum/k)
                sum=0
                k=0
            sal.append(vrms)      
        val=np.average(np.array(sal))
        return sal,val

    def normSignal(self,v):
        """
        Funcion para normalizar la señal de tension. Amplitud centrada en 1
        :Param: v señal de entrada
        :Return: vector de salida normalizada
        """
        #filtro pasa bajos Tc=27,3s.
        vrms,_ = self.rms(v)
        zi1 = signal.lfilter_zi(self.z1, self.p1)
        z,h = signal.lfilter(self.z1, self.p1, vrms,zi=zi1*vrms[0])
        z=z*np.sqrt(2)
        vo=v/z
        return vo

    def normSignalWoFil(self,v):
        """
        Funcion para normalizar la señal de tension. Amplitud centrada en 1
        Sin aplicar filtro. Tomo todo el array y lo promedio para sacar rms
        :Param: v señal de entrada
        :Return: vector de salida normalizada
        """
        arrms,vrms = self.rms(v)
        #print(vrms)
        vrms=vrms*np.sqrt(2)
        vo=v/vrms
        return vo

    def filters(self,v):
        """
        Funcion que implementa los bloques 2, 3 y 4
        :Param: v vector de valores normalizados
        """
        # Primer paso entrada al cuadrado bloque 2
        v=v**2
        # Aplico primer filtro pasa banda bloque 3
        zi2 = signal.lfilter_zi(self.z2,self.p2)
        z,h = signal.lfilter(self.z2,self.p2,v,zi=zi2*v[0])
        # Aplico segundo filtro bloque 3
        zi3 = signal.lfilter_zi(self.z3,self.p3)
        z,h = signal.lfilter(self.z3,self.p3,z,zi=zi3*z[0])
        # cuadrado y filtro bloque 4
        z=z**2
        # Segundo paso smoothing
        zi4 = signal.lfilter_zi(self.z4,self.p4)
        z,h = signal.lfilter(self.z4,self.p4,z,zi=zi4*z[0])
        # Multiplicador
        z = z*1.24e6
        return z

    def percentil(self,ps,percentil ):
        """
        Funcion de calculo de percentil modificado segun ecuacion de la norma
        Esta funcion solo la llama la funcion flicker
        :Param: ps arreglo generado en la funcion flicker
        :percentil: valor de percentil a calcular
        """
        num_class=len(ps[0,:])
        full_range=np.amax(ps[2,:])-np.amin(ps[1,:])
        n=0
        yk=0
        yn_1=0
        yn=0
        for j in range(num_class):
            if (percentil>=ps[3,j]):
                yn=ps[3,j] # valor inferior de la clase
                if j!=1:
                    yn_1=ps[3,j-1]  # valor frecuencia acumulada clase anterior
                else:
                    yn_1=100
                yk=percentil
                n=j
                break
        
        p=(full_range/num_class)*(n-(yk-yn)/(yn_1-yn))+np.amin(ps[1,:])   #   Li+(k-fi_1)*amp/fi; %calculo del percentil
        return p
    
    def flicker(self,pinst,num_class):
        """
        Funcion de calculo de valor de flicker
        """
        pint_max=np.amax(pinst)
        pint_min=np.amin(pinst)
        val_class=(pint_max-pint_min)/num_class
        ps=np.zeros((4,num_class))
        for j in range(num_class):
            for i in pinst:
                if i>=(pint_min+val_class*j) and i<(pint_min+val_class*(j+1)):
                    ps[0,j]=ps[0,j]+1
            ps[0,j]=(ps[0,j]/len(pinst))*100
            ps[1,j]=pint_min+val_class*j
            ps[2,j]=pint_min+val_class*(j+1)
        
        # Calculo de probabilidad acumulativa inversa*
        ps[3,0]=100-ps[0,0]
        for j in range(1,num_class):
            ps[3,j]=ps[3,j-1]-ps[0,j]
        # Calculo de los percientiles
        perc=np.zeros((20))
        perc[1]=self.percentil(ps,0.1)
        perc[2]=self.percentil(ps,0.7)
        perc[3]=self.percentil(ps,1)
        perc[4]=self.percentil(ps,1.5)
        perc[5]=self.percentil(ps,2.2)
        perc[6]=self.percentil(ps,3)
        perc[7]=self.percentil(ps,4)
        perc[8]=self.percentil(ps,6)
        perc[9]=self.percentil(ps,8)
        perc[10]=self.percentil(ps,10)
        perc[11]=self.percentil(ps,13)
        perc[12]=self.percentil(ps,17)
        perc[13]=self.percentil(ps,30)
        perc[14]=self.percentil(ps,50)
        perc[15]=self.percentil(ps,80)

        perc[16]=(perc[2]+perc[3]+perc[4])/3
        perc[17]=(perc[5]+perc[6]+perc[7])/3
        perc[18]=(perc[8]+perc[9]+perc[10]+perc[11]+perc[12])/5
        perc[19]=(perc[13]+perc[14]+perc[15])/3
        pst=np.sqrt(0.0314*perc[1]+0.0525*perc[16]+0.0657*perc[17]+0.28*perc[18]+0.08*perc[19])     
        return (ps,perc,pst)
    
    def VficticiaSim(self,Rc,Lc,Fm,Fi0,Fim,IWIND,tiempo ):
        """
        Genera la V ficticia segun IEC 61400-21 pero por simulacion
        :Param Rc: Vector con valores de resistencia ficticia, longitud igual a Lc
        :Param Lc: vector con valores de inductacia ficticia, longitud igual a Rc
        :Param Fm: frecuancia de inyeccion corriente
        :Param Fi0: angulo de la tension de linea
        :Param Fim: angulo de la corriente inyectada
        :Param IWIND: Corriente inyectada RMS vector c/1sg
        :Param tiempo: tiempo en segundos del vector de salida
        :Return Vfic: vector con la tension ficticia
        :Return im: corriente inyectada regenerada
        :Return u0: tension de linea regenerada
        :Return t: vector de tiempo
        """
        t = np.arange(0,tiempo,1/self.fs)
        
        if (len(Rc)<=len(Lc)):
            elem=len(Rc)
        else:
            elem=len(Lc)
            
        u0=np.zeros(len(t))
        im=np.zeros(len(t))
        Vfic=np.zeros([len(t),elem])
        k=0
        j=0
        for i in t:
            u0[j]=self.U_nom*1.41421*np.sin(2*np.pi*self.line_freq*i+Fi0)
            im[j]=IWIND[k]*1.41421*np.sin(2*np.pi*Fm*i+Fim)
            k=int(np.floor(i)) 
            j=j+1
        for l in range(elem):
            j=0
            im_ant=0
            for i in t:
                VL=Lc[l]*self.fs*(im[j]-im_ant)
                im_ant=im[j]
                Vfic[j,l]=u0[j]+Rc[l]*im[j]+VL
                j=j+1
                
        return Vfic, im, u0, t
    
    def Vficticia(self,Rc,Lc,Uo,Im ):
        """
        Genera la V ficticia segun IEC 61400-21 
        :Param Rc: Valor de resistencia del sistema en ohms
        :Param Lc: Valor de inductacia del sistema en Henrios
        :Param Uo: Vector con la tension registrada de linea
        :Param Im: Corriente de linea registrada
        :Return Vfic: vector con la tension ficticia
        
        """
               
        if (len(Uo)!=len(Im)):
            return "Vectores no concuerdan"
        
        n = np.arange(0,len(Uo),1)   
        Vfic=np.zeros(len(Uo))
        Im_ant=0
        for i in n:
            VL=Lc*self.fs*(Im[i]-Im_ant)
            Im_ant=Im[i]
            Vfic[i]=Uo[i]+Rc*Im[i]+VL
                
        return Vfic


