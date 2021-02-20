import subprocess
import os
import time
import Adafruit_DHT as dht

from gpiozero import OutputDevice


HIGH_THRESHOLD_CORE = 48
LOW_THRESHOLD_CORE = 39  
GPIO_PIN_CORE = 16
fanCore=0

SLEEP_INTERVAL= 5

HIGH_THRESHOLD_DHT = 24
LOW_THRESHOLD_DHT = 22  
GPIO_PIN_DHT = 21
fanDHT=0



def getTemp():
    output=os.popen("vcgencmd measure_temp").readline()
    h,tempDHT = dht.read_retry(dht.DHT22, GPIO_PIN_DHT)
    tempCore=float(output.split('=')[1].split('\'')[0])
    return tempCore,tempDHT 

if (LOW_THRESHOLD_CORE >= HIGH_THRESHOLD_CORE) or (LOW_THRESHOLD_DHT >= HIGH_THRESHOLD_DHT):
   raise RuntimeError('OFF_THRESHOLD must be less than ON_THRESHOLD')

fan = OutputDevice(GPIO_PIN_CORE)
fan.on()
while True:
    tempCore,tempDHT = getTemp()
    print(tempCore)
    print(tempDHT)
    if (tempCore >= HIGH_THRESHOLD_CORE and fanCore==0):
        fan.off()
        fanCore=1
    elif (tempCore <= LOW_THRESHOLD_CORE and fanCore==1):
        fan.on()
        fanCore=0
    elif (tempDHT >= HIGH_THRESHOLD_DHT and fanDHT==0):
        fan.off()
        fanDHT=1
    elif (tempDHT <= LOW_THRESHOLD_DHT and fanDHT==1):
        fan.on()
        fanDHT=0
    time.sleep(SLEEP_INTERVAL)

