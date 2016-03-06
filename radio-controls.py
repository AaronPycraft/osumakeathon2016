import serial
import time
from fm_tuner import fm_tuner
from threading import Timer
from threading import Thread

s = None
tb = fm_tuner()
curr_freq = 90.5e6
ave_mag = 0.0
def change_freq(new_freq):
    tb.rtlsdr_source_0.set_center_freq(new_freq)
t = Timer(10, change_freq, args=[992.5])
#t.start()


#thread = Thread(target=tb.Wait())
#thread.daemon = True

tb.Start(True)
#thread.start() #tb.Wait()


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
    if values[2] == "1":
        change_freq(90.5e6)
    if values[3] == "1":
        change_freq(92.3e6)
    if values[4] == "1":
        change_freq(91.1e6)
    if values[5] == "1":
        change_freq(91.1e6)
    if values[6] == "1":
        change_freq(max(curr_freq - 0.2e6, 87.9e6))
    if values[7] == "1":
        change_freq(min(curr_freq + 0.2e6, 107.9e6))

try:
    while True:
        curr_freq = tb.get_center_freq_probe()
        ave_mag = (9 * ave_mag + tb.get_ave_mag_probe())/10
        #print "Center Freq: %f\t\tAve Mag: %f" %(curr_freq, ave_mag)
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


