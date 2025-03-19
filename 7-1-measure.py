import RPi.GPIO as gpio
import time
import matplotlib.pyplot as plt
import matplotlib
gpio.setmode(gpio.BCM)
dac=[8, 11, 7 , 1, 0, 5, 12, 6]
gpio.setup(dac, gpio.OUT)
def dec2bin(n):
    return [int(x) for x in ("0"*(8-len(bin(n)[2::]))+bin(n)[2::])]
comp=14
troyka=13
gpio.setup(comp, gpio.IN)
gpio.setup(troyka,gpio.OUT, initial=1)
def adc():
        c=0
        for k in range(8):
            c+=2**(7-k)
            gpio.output(dac, dec2bin(c))
            time.sleep(0.001)
            if gpio.input(comp)==1:
                c-=2**(7-k)
        return (c)
value=[]
t0=time.time()
try:
    while adc()<206:
        gpio.output(troyka, 1)
        value.append(adc()*3.3/256)
        print(adc())
        
    while adc()>192:
        gpio.output(troyka, 0)
        value.append(adc()*3.3/256)
        print(adc())
        
finally:
    t1=time.time()
    gpio.output(dac, 0)
    gpio:gpio.cleanup()
    t=t1-t0
    T=t/len(value)
    f=1/T
    qs=3.3/256
    print('время:',t)
    print('период одного измерения:',T)
    print('средняя частота дискретизации:',f)
    print('шаг квантования:',qs)
    d=open('data.txt','w')
    s=open('settings.txt','w')
    d.write('\n'.join([str(x*256/3.3) for x in value]))
    s.write(str(f)+'\n')
    s.write(str(qs))
d.close()
s.close()
x=[]
for i in range(len(value)):
    x.append(T*i)
y=value
plt.plot(x,y)
plt.show()