import pyfirmata
import os
import sys
import time

pin = 13
port = 'COM4'
board = pyfirmata.Arduino(port)

board.digital[pin].write(1)
show = board.digital[pin].read()
soil_show = board.analog[0].read()

print	(soil_show)