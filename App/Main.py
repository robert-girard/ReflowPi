'''
ReflowPi

Copyright © <2019> <Robert Girard>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

from flask import Flask, render_template, request, jsonify, abort
import shelve
from support import Step, Profile
from flask_socketio import SocketIO, emit
import time, threading
import numpy as np
import Profile
from RunLoop import PIDloop

app = Flask(__name__)
app.config['SECRET_KEY']='secret!'
socketio = SocketIO(app)
testrun = PIDloop(socketio)

@socketio.on('connect')
def connected():
   print("%s connected" % (request.namespace))

@app.route('/')
@app.route('/Index')
def index():
   global testrun
   testrun.stop()
   profileBuffer = shelve.open("Profiles")
   profiles = profileBuffer.keys()
   return render_template('index.html', profiles=profiles)

@app.route('/Make')
@app.route('/Make/<pname>')
def makeProfile(pname=None):
   global testrun
   testrun.stop()
   if pname is None:
      return render_template('Make_Profile.html', profile=pname)
   profileBuffer = shelve.open("Profiles")
   if pname in profileBuffer:
      profile = profileBuffer[pname]
      return render_template('Make_Profile.html', profile=profile)
   else:
      profileBuffer.close()
      abort(404)

@app.route('/Save', methods = ['POST'])
def save_profile():
   content = request.get_json()
   saveProfile = Profile.Profile.fromdict(content)
   profileBuffer = shelve.open("Profiles")
   profileBuffer[saveProfile.name] = saveProfile
   profileBuffer.close()
   return "Profile Saved", 200

'''
@app.route('/Calibrate', methods = ['POST']) #TODO create PID tuning for calibration
def save_profile():
   content = request.get_json()
   saveProfile = Profile.Profile.fromdict(content)
   profileBuffer = shelve.open("Profiles")
   profileBuffer[saveProfile.name] = saveProfile
   profileBuffer.close()
   return "Profile Saved", 200
'''

@app.route('/Run')
@app.route('/Run/<pname>')
def runProfile(pname=None):
   global testrun
   testrun.stop()
   if pname is None:
      return render_template('Run_Profile.html', profile=pname)
   with shelve.open("Profiles") as profs:
      try:
         testrun.profile = profs[pname] #Chnage to lower case p profile
      except KeyError:
         abort(404)
   print(testrun.profile)
   return render_template('Run_Profile.html', profile=testrun.profile)

@socketio.on('run')
def funrun():
   global testrun
   global socketio
   if testrun.is_alive():
      testrun.resume()
   else:
      profile = testrun.profile
      del testrun
      testrun = PIDloop(socketio, p=profile)
      print("made IT")
      testrun.start()

@socketio.on('stop')
def funstop():
   global testrun
   testrun.stop()

@socketio.on('pause')
def funpause():
   global testrun
   testrun.pause()

if __name__ == '__main__':
   socketio.run(app, "0.0.0.0")
