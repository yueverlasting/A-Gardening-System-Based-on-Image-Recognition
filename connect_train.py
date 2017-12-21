import serial

s = serial.Serial('COM3',9600)
	
while	True:
	print (s.readline())