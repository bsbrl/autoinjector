# Autoinjector
-------------

The autoinjector is an automated computer vision guided platform to serially inject tissue with user parameter selection along a specified trajectory using a 3-axis micromanipulator. This read me takes you through the system requirements, install instructions, operating instructions, and how to customize the code based on different cameras. For a complete description of the device see the Autoinjector paper and supplementary materials. 

1. [System Requirements](https://github.com/ogshull/Autoinjector-/tree/PVCAM#system-requirements)
	- [Hardware Requirements](https://github.com/ogshull/Autoinjector-/tree/PVCAM#hardware-requirements)
	- [Software Requirements](https://github.com/ogshull/Autoinjector-/tree/PVCAM#software-requirements)
2. [Install Instructions](https://github.com/ogshull/Autoinjector-/tree/PVCAM#install-instructions)
	- Install Python 2.7.13
	- Install Arduino
	- Install Micromanager
	- Install Sensapex SDK
	- Install Python packages 

It is recommended to start in order. 

## System requirements 
-------------
A complete list of available cameras can be found at micromanager's device support (https://micro-manager.org/wiki/Device_Support). Manipulator support exists for Sensapex manipulators only. However, if the manipulators have available SDK, custom API can be made using Python's ctypes. Contact G. Shull for additional support for adapting SDKs for python use. 

### Hardware Requirements
1. Computer
2. Arduino Uno
3. Microscope (brightfield, phase contrast, or DIC)
4. Microscope camera (tested with Hamamatsu Orca Dcam, and Cool Snap Dyno PVCam)
5. Sensapex Three axis uMP Micromanipulator 
6. Custom pressure rig

### Software Requirements
Currently, the autoinjector is only available with Windows support. The following libraries are used in the Autoinjector software (see install instructions for how to install). 
- Python 2.7.12 
- Arduino 1.8
	- pip 
	- Native python libraties
		- time
		- sys
		- os
		- user
	- Matplotlib 2.0.0 +
	- MMCorePy 1.4.22+ (Micromanager python API)
	- NumPy 1.12.0 +
	- OpenCV 3.1.0 +
	- Pyserial 
	- PyQt 4.11.14 +
	- Sensapex API
	- scikit-image 0.13.0 +
	- Scipy 0.19.0 +
- Micromanager 1.4.22 +
- Sensapex SDK
- Your camera driver

## Install Instructions
-------------
Install the following software to operate the Autoinjector. It is recommended to install the software in the order it is listed. Make sure to run every file as administrator (right click, "Run as administrator")! Otherwise, the install may fail. 

### Python
1. Download the python windows installer [here](https://www.python.org/downloads/release/python-2713/). 
2. Launch the installer and follow installation instructions on screen.
3. Add Python to system environment path by following [these instructions](https://superuser.com/questions/143119/how-do-i-add-python-to-the-windows-path) so that you can run python from any windows command prompt.

#### Python Packages
1. Pip (python installer package). Follow instructions [here](https://github.com/BurntSushi/nfldb/wiki/Python-&-pip-Windows-installation#pip-install) to download PIP. 

### Arduino
1. Download the arduino windows installer [here](https://www.arduino.cc/en/Main/Software?).
2. Launch the installer and follow installation instructions on screen.

### Micromanager
1. Download the micromanager windows installer [here](https://micro-manager.org/wiki/Download_Micro-Manager_Latest_Release).
2. Launch the installer and follow installation instructions on screen.

### Sensapex SDK
1.... Need to figure out how to distrubute SDK

### Autoinjector Software 
1. Download or clone this repository by clicking "Clone or Download" button on the topright area of the [Autoinjector Respository](https://github.com/ogshull/Autoinjector-/tree/PVCAM) and extract the files. 
2. Open command prompt (make sure to run as administrator).
3. Download Python packages (for more info/support, click the names of the packages). To download the python packages run the following commands from the command prompt:
	- [Matplotlib](https://matplotlib.org/users/installing.html#windows)
		```
		python -m pip install matplotlib
		```
		
	- [NumPy](http://www.numpy.org/)
		```
		python -m pip install numpy
		```

	- OpenCV 3.1.0 +
	- Pyserial 
	- PyQt 4.11.14 +
	- Sensapex API
	- scikit-image 0.13.0 +
	- Scipy 0.19.0 +


## Running the Application

 To run the program click the file "launchapp.py" in the main directory. This will launch the GUI and report any errors with hardware.

## License

This work is lisenced under the MIT lisence. See LISENCE.txt for additional information.  
