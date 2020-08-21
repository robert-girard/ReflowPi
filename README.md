ReflowPi
=============================================
*Created by Robert Girard*

---------------------------------------------

## About
Conversion of a toaster oven into ad hoc reflow oven using RasperryPI. The App itself is served to the local network using Flask/HTML/JS/CSS so that a screen is not required for final usage.

### The Boards
Initially a PCB [Board v0.1](Design/Board_v0.1) was designed to power the RaspberryPi and monitor as well as contain the SCR output control, gate triggering, level shifting, SPI thermocouple interface and PWM fan control for two fans (one cooling and one convection). 

Board v0.1 was functional but due to an unfortunate wiring incident the SCRs were connected improperly and the protection diodes were shorted damaging the PCB. The output was then rerouted to an SSR to control the oven for further testing. Testing indicated that the ramp rate was sufficent without convection so the Fans were omitted for simplicity in the next iteration.

The second iteration ([Board v1.0](Design/Oven_Final/Board_v1.0)) was simplified further by using commercial power adapters and SSR output control.

### The Oven
The Reflow oven itself was a commercial off the shelf toaster oven rated at ~10 A. Wet and Stick Fiberglass Insulation (McMaster-Carr 87945K1) was added to the exterior of the oven compartment. No modifications to the heating elements. [Images seen here.](Design/Oven_Final)

### The Code
Originally A PyQt5 app was developed for the touchscreen but I decided that it would be nicer to work from a desktop or phone so the applicaiton was ported to a Flask web app. The PyQt5 app, though functional if not totally complete, is not included mostly due to me not wanting to look up the licencing sorrounding PyQt5.

The web app allows for creation, modification, and running of profiles remotely. [Chart.js](https://www.chartjs.org/) was used to display profile data. [Bootstrap4](https://getbootstrap.com/), [jquery](https://jquery.com/) and other various javascript modules were used to create a (reasonably) appealing interface that is responsive to mobile and desktop browsing. [Flask-SocketIo](https://flask-socketio.readthedocs.io/en/latest/) handles the communication of packaged JSON data between the server and client.

the [simple-pid](https://github.com/m-lundberg/simple-pid) library handles PID control of the reflow oven while [RPi-GPIO](https://pypi.org/project/RPi.GPIO/#files) and [py-spydev](https://github.com/doceme/py-spidev) iterface low level control of the RasperryPI periferals. Source Code for the full project can be found [here](App/). Though functional the code could use some TLC and housecleaning. There is also a list of proposed additions below.

## Installation and Usage

### RaspberryPi Setup
*Requires mouse/keyboard/screen to be connected to RaspberryPi*

- Install Rasbian OS
- Setup RaspberryPi to run on you network ([Example Setup](https://raspberrypihq.com/how-to-connect-your-raspberry-pi-to-wifi/#:~:text=Configuring%20your%20WiFi%20network,conf.&text=Remember%20to%20replace%20this%20with,Ctrl%2BX%20followed%20by%20Y.))
	- Note the IP address of your Pi: `<PiIP>`
- Install Python (3.7)
- Install Packages from Dependancies list below
- Place the [Flask_Workspace](Flask_Workspace/) in your prefered location
	- **Note:** This Folder also contains the workspace files for VS Code if you would like to modify the project 
- Connect Board_v1.0 to RaspberryPI.
- Connect Thermocouple and SSR to Board_v1.0.
- Connect Heating Element to SSR.

### Python Dependancies
Just pip3 them. Links provided for completeness sake.
- Flask ([Link](https://flask.palletsprojects.com/en/1.1.x/))
- Flask-SocketIO ([Link](https://flask-socketio.readthedocs.io/en/latest/))
- RPi.GPIO ([Link](https://pypi.org/project/RPi.GPIO/))
- Numpy ([Link](https://numpy.org/install/))

### Usage
- Run `Main.py` with `sudo python3 <Your_folder_location>/folder/Main.py`
- Access the webpage from your phone or desktop at:  `http://<PiIP>:50000`
	- **Note:** port 5000 is the default port of the flask test server and may vary
- Create profile or use existing test Profiles.
- Get Reflowing!

#### Alternatively
- Setup RaspberryPi to run MAIN.py on boot using your preferred [method](https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/) 
- Now you no longer need mouse/keyboard/screen connected to the RaspberyPi!


## License
- ReflowPi is served on an MIT License.

## Potential Improvements
- Use a proper WSGI (e.g. Apache) to serve the app instead of the flask developement server.
- PID auto-tune functionality.
- Calibration interface for thermocouple input.
- prettier interface. (Currently looks better on mobile then desktop)
- Additional Insulation/higher power for better Ramp Rate.

