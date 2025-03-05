import RPi.GPIO as GPIO
import time 
dac = [8,11,7,1,0,5,12,6]
comp=14
troyka=13
GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(comp, GPIO.IN)
GPIO.setup(troyka,GPIO.OUT,initial=GPIO.HIGH)
def d2b(value):
 return [int(bit) for bit in bin(value)[2:].zfill(8)]
def n2d(v):
    s=d2b(v)
    GPIO.output(dac,s)
    time.sleep(0.001)
    return s
def adc():
    for val in range(256):
        s=n2d(val)
        cv=GPIO.input(comp)
        if cv==1:
            vol=val*3.3/256
            print(val,s,vol)
            break
        if val==255:
            vol=3.3
            print(val,s,vol)
            break
try:
    while True:
        adc()
finally:
    GPIO.output(dac,0)
    GPIO.cleanup()
