import serial
import time
from fm_tuner import fm_tuner
from threading import Timer

s = None
tb = fm_tuner()

def change_freq(new_freq):
    tb.rtlsdr_source_0.set_center_freq(new_freq)

tb.Start(True)

def processInputs(values):
    if values[2] == "1":
        change_freq(90.5e6)
    if values[3] == "1":
        change_freq(92.3e6)
    if values[4] == "1":
        change_freq(91.1e6)

try:
    while True:
        if not s:
            try:
                s = serial.Serial("/dev/ttyACM0", 9600)
            except:
                s = None
            time.sleep(0.05)
        else:
            try:
                if s.inWaiting() > 1:
                    value = s.readline().strip()
                    print value
                    processInputs(value.split(","))
            except:
                s = None
            time.sleep(0.05)
except KeyboardInterrupt:
    s.close()


