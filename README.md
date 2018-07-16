# Autoinjector
-------------

The autoinjector is an automated computer vision guided platform to serially inject tissue with user parameter selection along a specified trajectory using a 3-axis micromanipulator. This read me takes you through the system requirements, install instructions, operating instructions, and how to customize the code based on different cameras. For a complete description of the device see the Autoinjector paper and supplementary materials. 

1. [System Requirements](https://github.com/ogshull/Autoinjector-/tree/PVCAM#system-requirements)
	- [Hardware Requirements](https://github.com/ogshull/Autoinjector-/tree/PVCAM#hardware-requirements)
	- [Software Requirements](https://github.com/ogshull/Autoinjector-/tree/PVCAM#software-requirements)
2. [Install Instructions](https://github.com/ogshull/Autoinjector-/tree/PVCAM#install-instructions)
3. [Running the Application](https://github.com/ogshull/Autoinjector-/tree/PVCAM#running-the-application)
4. [License](https://github.com/ogshull/Autoinjector-/tree/PVCAM#license)

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
1. [Python 2.7.12](https://github.com/ogshull/Autoinjector-/tree/PVCAM#1-python)
	- [Packages](https://github.com/ogshull/Autoinjector-/tree/PVCAM#python-packages)
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
2. [Arduino 1.8](https://github.com/ogshull/Autoinjector-/tree/PVCAM#2-arduino)
3. [Micromanager 1.4.22 +](https://github.com/ogshull/Autoinjector-/tree/PVCAM#3-micromanager)
4. [Sensapex SDK](https://github.com/ogshull/Autoinjector-/tree/PVCAM#4-sensapex-sdk)
5. [The Autoinjector software](https://github.com/ogshull/Autoinjector-/tree/PVCAM#5-autoinjector-software)
6. [Your camera driver](https://github.com/ogshull/Autoinjector-/tree/PVCAM#6-your-camera-driver)

## Install Instructions
-------------
Install the following software to operate the Autoinjector. It is recommended to install the software in the order it is listed. Make sure to run every file as administrator (right click, "Run as administrator")! Otherwise, the install may fail. 

### 1. Python
1. Download the python windows installer [here](https://www.python.org/downloads/release/python-2713/). 
2. Launch the installer and follow installation instructions on screen.
3. Add Python to system environment path by following [these instructions](https://superuser.com/questions/143119/how-do-i-add-python-to-the-windows-path) so that you can run python from any windows command prompt.

	#### Python Packages
	1. Pip (python installer package). 
		1. Download [get-pip.py](https://bootstrap.pypa.io/get-pip.py) (Right click and click "save as" to download the file).
		2. Open the file in your downloads folder and click the file, this will download pip. It will not give you any confirmation, a window will pop up and disappear. Pip will have loaded after this is complete. If pip did not load successfully you will see an error in the following steps. 

	2. To download the python packages run the following commands from the command prompt (for more info/support, click the names of the packages):
		- [Matplotlib](https://matplotlib.org/users/installing.html#windows)
			```
			python -m pip install matplotlib
			```

		- [NumPy](http://www.numpy.org/)
			```
			python -m pip install numpy
			```

		- [OpenCV](https://pypi.org/project/opencv-python/3.1.0/)
			```
			python -m pip install opencv-python
			```

		- [Pyserial](https://github.com/pyserial/pyserial)
			```
			python -m pip install pyserial
			```

		- [scikit-image](http://scikit-image.org/docs/dev/install.html)
			```
			python -m pip install scikit-image
			```

		- [Scipy](https://www.scipy.org/install.html)
			```
			python -m pip install scipy
			```

		- [PyQt](http://pyqt.sourceforge.net/Docs/PyQt4/installation.html)
			PyQt4 is the only one which we cannot download with pip. To install it, do the following:
			1. Download the file "PyQt4‑4.11.4‑cp27‑cp27m‑win_amd64.whl" if you have a 64-bit system, or "PyQt4‑4.11.4‑cp27‑cp27m‑win32.whl" if you have a 32-bit system from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyqt4) 
			2. Run the command prompt as administrator and navigate to your downloads folder. I.e. 
			```
			cd C:\Users\Gabi\Downloads
			```
			3. Type the following code to download pyqt4 (if you have the 32-bit system change the filename to the one from step 1):
			```
			python -m pip install PyQt4‑4.11.4‑cp27‑cp27m‑win_amd64.whl
			```

### 2. Arduino
1. Download the arduino windows installer [here](https://www.arduino.cc/en/Main/Software?).
2. Launch the installer and follow installation instructions on screen.

### 3. Micromanager
1. Download the micromanager windows installer [here](https://micro-manager.org/wiki/Download_Micro-Manager_Latest_Release).
2. Launch the installer and follow installation instructions on screen.

### 4. Sensapex SDK
1. TBD

### 5. Autoinjector Software 
1. Download or clone this repository by clicking "Clone or Download" button on the top right area of the [Autoinjector Respository](https://github.com/ogshull/Autoinjector-/tree/PVCAM) and extract the files. 

2. Upload arduino code:
	1. Once the arduino is installed, connect your arduino to your computer via USB.
	2. In the downloaded Autoinjector folder, open the file "Autoinjector-\pythonarduino\pythonarduinotriggeropen.ino"
	3. Follow the instructions to identify your port and connect to the arduino from the arudino software as shown in [this tutorial](https://www.arduino.cc/en/Guide/ArduinoUno#toc5). Take note of which COM port your arduino is on i.e. COM6.
	4. Upload the pythonarduinotriggeropen.ino file as shown in [this tutorial](https://www.arduino.cc/en/Guide/ArduinoUno#toc6).

3. Test autoinjector code:
	1. Run the command prompt as administrator
	2. Navigate to the folder of the downloaded and extracted zip file. For example, if I extracted the zipped download to "C:\Users\Gabi\Downloads\Autoinjector-" I would go to this directory in the command prompt by typing:
		```
		cd C:\Users\Gabi\Downloads\Autoinjector-
		```
	3. To test that the software was downloaded properly, type:
		```
		python launchapp.py
		```
		This will launch the Autoinjector and report any problems to the command prompt if there is an error in the downloaded sotware. 

### 6. Your Camera Driver
Follow the instructions for your camera driver install. In our work we have used the [Hamamatsu Orca Camera](https://www.hamamatsu.com/us/en/product/type/C13440-20CU/index.html) and [Photometrics Cool Snap Dyno PVCam](https://www.photometrics.com/products/ccdcams/coolsnap-dyno.php)

## Running the Application
---------

 To run the program normally, click the file "launchapp.py" in the Autoinjector folder. This will launch the GUI and report any errors with hardware. For additional operating instructions see the user manual included with the publication.

## License
-------------
This work is lisenced under the MIT lisence. See LISENCE.txt for additional information.  
