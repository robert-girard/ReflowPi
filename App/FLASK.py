'''
ReflowPi

Copyright © <2019> <Robert Girard>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

@app.route('/Delete/<pname>')
def deleteProfile(pname):
    if profileBuffer.get(pname, "Not Found") == "Not Found":
        abort(404)
    else:
        #deleteprofile and reload buffer
        profiles = None #getprofilenamesafterdeletion
        return render_template('ProfileOptions.html', Profiles=profiles) #change to whatevs

@app.route('/Make')
@app.route('/Make/<pname>')
def deleteProfile(pname=None):
    if pname is None:
        return render_template('Make.html')
    elif profileBuffer.get(pname, "Not Found") == "Not Found":
        abort(404)
    else:
        chartData  = None #make this do somthing
        return render_template('Make.html', data=chartData)

@app.route('/Run')
@app.route('/run/<pname>')
def deleteProfile(pname=None):
    if pname is None:
        abort(400)
    elif profileBuffer.get(pname, "Not Found") == "Not Found":
        abort(404)
    else:
        chartData  = None 
        return render_template('Run.html', data=chartData)

@app.route('/ProfileOptions')
def getProfileOptions():
    profiles = None #getprofilenamesafterdeletion
    return render_template('ProfileOptions.html', Profiles=profiles) #change to whatevs