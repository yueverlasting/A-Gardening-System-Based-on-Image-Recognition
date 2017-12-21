import time
import sys
import signal

from PyMata.pymata import PyMata

# Digital pin 13 is connected to an LED. If you are running this script with
# an Arduino UNO no LED is needed (Pin 13 is connected to an internal LED).
BOARD_LED = 13

# Create a PyMata instance
board = PyMata("COM4", verbose=True) #定義板子跟阜

def signal_handler(sig, frame):    #副函式
    print('You pressed Ctrl+C')
    if board is not None:
        board.reset()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Set digital pin 13 to be an output port
board.set_pin_mode(BOARD_LED, board.OUTPUT, board.DIGITAL)

time.sleep(2)
print("Blinking LED on pin 13 for 10 times ...")

# Blink for 10 times
for x in range(10):
    print(x + 1)
    # Set the output to 1 = High
    board.digital_write(5, 1)
    # Wait a half second between toggles.
    time.sleep(5)
    # Set the output to 0 = Low
    board.digital_write(5, 0)
    time.sleep(5)

# Close PyMata when we are done
board.close()