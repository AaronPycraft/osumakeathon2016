import serial
import time
from fm_tuner import fm_tuner
from threading import Timer
from threading import Thread
import math


preset1 = 90.5E6
preset2 = 92.3E6

s = None
tb = fm_tuner()
tb.Start()
enabled = False
print "*********"
print enabled
curr_freq = preset1
ave_mag = 0.0
curr_volume = 1
def change_freq(new_freq):
    if enabled:
        tb.rtlsdr_source_0.set_center_freq(new_freq)
        curr_freq = new_freq


"""fp = open("station-magnitudes.csv", "w")
for _freq in xrange(879, 1079, 2):
    freq = _freq * 10**5
    change_freq(freq)
    time.sleep(4.0)
    ave_mag = 0
    for i in range(20):
        ave_mag += tb.get_ave_mag_probe()
        time.sleep(0.1)
    ave_mag = ave_mag / 20
    print "Center Freq: %f\t\tAve Mag: %f" %(freq, ave_mag)
    fp.write("%f,%f\n" %(freq, ave_mag))
fp.close()
exit()"""


def processInputs(values):
    global tb
    global enabled
    global preset1
    global preset2
    global curr_volume
    if len(values) != 10:
        return
    if values[1] == "1":
        change_freq(preset1)
    if values[2] == "1":
        change_freq(preset2)
    if values[3] == "1":
        change_freq(max(curr_freq - 0.2e6, 87.9e6))
    if values[4] == "1":
        change_freq(min(curr_freq + 0.2e6, 107.9e6))
    if values[5] == "1":
        change_freq(max(curr_freq - 0.2e6, 87.9e6))
    if values[6] == "1":
        change_freq(min(curr_freq + 0.2e6, 107.9e6))
    if values[7] == "1":
        preset1 = curr_freq
    if values[8] == "1":
        preset2 = curr_freq
    if values[9] == "1":
        if enabled:
            enabled = False
        else:
            enabled = True
        #print(enabled)

    new_volume = float(int(values[0])) * 2 / 1024
    #print("vol: %f, %f" %(curr_volume, new_volume))
    if not enabled and curr_volume != 0:
        tb.set_volume(0)
        curr_volume = 0
    elif enabled and new_volume != curr_volume:
        tb.set_volume(new_volume)
        curr_volume = new_volume




try:
    while True:
        if enabled:
            curr_freq = tb.get_center_freq_probe()
            ave_mag = (9 * ave_mag + tb.get_ave_mag_probe())/10
            print "Center Freq: %f\t\tAve Mag: %f" %(curr_freq, ave_mag)
        if not s:
            try:
                s = serial.Serial("/dev/ttyACM0", 9600)
            except serial.SerialException:
                s = None
            time.sleep(0.05)
        else:
            try:
                if s.inWaiting() > 1:
                    value = s.readline().strip()
                    #print value
                    processInputs(value.split(","))
            except serial.SerialException:
                s = None
            time.sleep(0.05)
except KeyboardInterrupt:
    s.close()


