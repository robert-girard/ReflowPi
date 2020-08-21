'''
ReflowPi

Copyright © <2019> <Robert Girard>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''


import time
import spidev
import atexit

class Thermo():
    spi = spidev.SpiDev()
    def __init__(self, cal=0):
        self.spi.open(0,0)
        self.cal = cal
    def readTemp(self):
        resp = self.spi.xfer2([0xff, 0xff, 0xff, 0xff])
        time.sleep(0.01)                            #How much delay? if lots maybe thread it
        sign = (resp[0] & 0x80)>>7
        resp[0] = resp[0] & 0x7f
        temp = (sign-1)*-1*(resp[0]*2**4 + ((resp[1]&0xf0)>>4) + ((resp[1]&0x0f)>>2)*2**-2)
        a = (resp[0]&0x7F) * (2**6)
        b = (resp[1]>>2)
        c = a+b
        if c >= 0b1111000011000:
            c = c-0b11111111111111 - 1
        c = c*0.25
        d = ((resp[2]&0x7F)*2**5 + (resp[3]>>4))*2**-4
        return temp+self.cal
    def __del__(self):
        self.spi.close()
        print("spi closed")

#atexit.register(Heater._CleanUp)

