import serial.rs485
ser=serial.rs485.RS485(port='/dev/ttyAMA0',baudrate=0)
ser.rs485_mode=serial.rs485.RS485Settings(True,False)
ser.write('me la soban'.encode('utf-8'))
#ser.write([3,176,4,0,0,183])
while True:
	c=ser.read(1)
	ser.write(c)
	print(c)

