'''
ReflowPi

Copyright © <2019> <Robert Girard>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

import threading
import time
import numpy as np
from simple_pid import PID
import math
from Thermo import Thermo
from Heater import Heater
import Profile


MAX_TEMP = 290
AMB = 20

class PIDloop(threading.Thread):

	def __init__(self, socket, tempcal=0, p=None):
		#self.daemon = True
		self.tccal = tempcal
		self.socket = socket
		self.stopEvent = threading.Event()
		self.stopEvent.clear()
		self.pauseEvent = threading.Event()
		self.pauseEvent.set()
		if p is not None:
			self.profile = p
		else:
			self.profile = Profile.Profile(None,[])
		self.init_PID()
		super().__init__()

	def init_PID(self):
		self.K = 50
		self.I = 10
		self.D = 5

		self.Heater = Heater()
		self.Thermo = Thermo(self.tccal)
		self.Heater.startHeat(0)

		for _ in range(5):
			print("TC read: ",self.Thermo.readTemp())

		self.T = np.array([self.Thermo.readTemp()])	#change this initial temp to a read
		self.t = np.array([0])
		self.c = []
		self.pid = PID(self.K,self.I,self.D, 0)
		self.pid.output_limits = (0, 1)
		self.pid.sample_time = 1
		power = self.pid(self.T[-1])
		self.c.append(power)

	def stop(self):
		self._clearControl()
		self.stopEvent.set() #set heater to off

	def pause(self):
		self.pauseEvent.clear()

	def resume(self):
	   self.pauseEvent.set()

	#mabye use? http://code.activestate.com/recipes/465057-basic-synchronization-decorator/
	#or https://stackoverflow.com/questions/29402606/possible-to-create-a-synchronized-decorator-thats-aware-of-a-methods-object
	def run(self):
		self.running = True
		self.stopEvent.clear()
		for i, step in enumerate(self.profile):
			intervals = np.linspace(float(step.startTemp), float(step.endTemp), step.Duration)
			tr = int(step.Duration)
			for interval in intervals:
				loopstart = time.time()
				self.pid.setpoint = interval
				pwr = self.pid(self.T[-1])
				tr -= 1
				print("power: ", pwr)
				self.Heater.UpdateHeaterDuty(pwr*100)
				self.t = np.append(self.t, [self.t[-1]+1])
				self.T = np.append(self.T, [self.Thermo.readTemp()])
				packet = {
					"point" : {
						"x": str(self.t[-1]),
						"y": str(self.T[-1])
					},
					"timeRemaining": str(tr),
					"SP": str(interval),
					"PV": str(self.T[-1]),
					"step": str(i+1)
				}
				self.socket.emit('update', packet)
				looptime = time.time()-loopstart
				if looptime < 1:
					time.sleep(1-looptime)
				#self.pauseEvent.wait()
				if self.stopEvent.is_set():
					return


	def ovenmodel(self, temp, power):
		'''To Simulate reflow oven time step'''
		mt = MAX_TEMP
		sh = 0.012
		temp = power*mt+ AMB - (power*mt-temp+AMB)*math.exp(-sh*1)
		return temp
	
	def _clearControl(self):
		self.Heater.stopHeater()
		return
