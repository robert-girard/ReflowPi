import RPi.GPIO as GPIO
import numpy as np
from threading import Lock
import atexit

class Heater():
    hwlock = Lock() #Lock in destructor not particularly good idea
    def __init__(self):
        self.Fan = 33
        self.Heat = 31
        Heater.hwlock.acquire()
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.Fan,GPIO.OUT)
        GPIO.setup(self.Heat,GPIO.OUT)
    def startHeat(self, h=1):
        self.dc = np.clip(h,0,1)
        self.heater = GPIO.PWM(self.Heat,1)
        self.heater.start(h)
    def startFan(self, f=1):
        self.dc = np.clip(f,0,1)
        self.fan = GPIO.PWM(self.Fan,20000)
        self.fan.start(f)
    def UpdateHeaterDuty(self, h):
        self.heater.ChangeDutyCycle(h)
    def UpdateFanDuty(self, f):
        self.fan.ChangeDutyCycle(f)
    def stopHeater(self):
        self.heater.stop()
    def stopFan(self):
        self.fan.stop()
    def __del__(self):
        self.heater.stop()
        GPIO.cleanup()
        Heater.hwlock.release() #Lock in destructor not particularly good idea
    @staticmethod
    def _CleanUp():
        GPIO.cleanup()
        pass

atexit.register(Heater._CleanUp)



    
        
