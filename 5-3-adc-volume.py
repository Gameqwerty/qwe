import RPi.GPIO as GPIO
import time 
dac = [8,11,7,1,0,5,12,6]
leds=[2,3,4,17,27,22,10,9]
comp=14
troyka=13
GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(leds, GPIO.OUT)
GPIO.setup(comp, GPIO.IN)
GPIO.setup(troyka,GPIO.OUT,initial=GPIO.HIGH)
def d2b(value):
 return [int(bit) for bit in bin(value)[2:].zfill(8)]
def n2d(v):
    s=d2b(v)
    #print(s)
    GPIO.output(dac,s)
    time.sleep(0.002)
    return s
def adc():
    a=[]
    val=0
    for i in range(8):
        #print(val)
        s=n2d(val+2**(8-i-1)-1)
        cv=GPIO.input(comp)
        if cv==0:
            val=val+2**(8-i-1)
            a.append(1)
            #GPIO.output(leds[i],1)
        else :
            a.append(0)
            #GPIO.output(leds[i],0)

        
    vol=val*3.3/256
    print(val,a,vol)
    return val
try:
    while True:
        f=adc()
        if f==0:
            c=0
        else:
            c=int(f/32)+1
        #print(c)
        a=d2b(2**c-1)
        GPIO.output(leds,a)
finally:
    GPIO.output(dac,0)
    GPIO.cleanup()