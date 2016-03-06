import serial

s = None


try:
    while True:
        if not s:
            try:
                s = serial.Serial("/dev/msp", 9600)
            except:
                s = None
        else:
            try:
                if s.inWaiting() > 1:
                    value = s.readline().strip()
                    print value
            except:
                s = None
except KeyboardInterrupt:
    s.close()
