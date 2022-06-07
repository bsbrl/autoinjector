# Autoinjector - Python 3 Version
-------------

The autoinjector is an automated computer vision guided platform to serially inject tissue with user parameter selection along a specified trajectory using a 3-axis micromanipulator. This read me takes you through the system requirements, install instructions, operating instructions, and how to customize the code based on different cameras. For a complete description of the device see the Autoinjector paper and supplementary materials. 

1. [System Requirements](https://github.com/bsbrl/autoinjector/tree/Python3#system-requirements)
	- [Hardware Requirements](https://github.com/bsbrl/autoinjector/tree/Python3#hardware-requirements)
	- [Software Requirements](https://github.com/bsbrl/autoinjector/tree/Python3#software-requirements)
2. [Install Instructions](https://github.com/bsbrl/autoinjector/tree/Python3#install-instructions)
3. [Running the Application](https://github.com/bsbrl/autoinjector/tree/Python3#running-the-application)
4. [License](https://github.com/bsbrl/autoinjector/tree/Python3#license)

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
1. [Python 3.7.5](https://github.com/bsbrl/autoinjector/tree/Python3#1-python)
	- [Packages](https://github.com/bsbrl/autoinjector/tree/Python3#python-packages)
		- pip 
		- Native python libraties
			- time
			- sys
			- os
			- user
		- Matplotlib 3.5.2
		- pymmcore 10.1.1.70.5
		- NumPy 1.21.6
		- OpenCV 4.5.5.64
		- Pyserial 3.5
		- PyQt 6.3.0
		- Sensapex 1.22.4
		- scikit-image 0.19.2
		- Scipy 1.7.3
2. [Arduino 1.8](https://github.com/bsbrl/autoinjector/tree/Python3#2-arduino)
3. [Micromanager 2.0 +](https://github.com/bsbrl/autoinjector/tree/Python3#3-micromanager)
4. [Sensapex SDK](https://github.com/bsbrl/autoinjector/tree/Python3#4-sensapex-sdk)
5. [The Autoinjector software](https://github.com/bsbrl/autoinjector/tree/Python3#5-autoinjector-software)
6. [Your camera driver](https://github.com/bsbrl/autoinjector/tree/Python3#6-your-camera-driver)
7. [Sensapex SDK](https://www.sensapex.com/products/ump-micromanipulation-system/)

## Install Instructions
-------------
Install the following software to operate the Autoinjector. It is recommended to install the software in the order it is listed. Make sure to run every file as administrator (right click, "Run as administrator")! Otherwise, the install may fail. 

### 1. Python
1. Download the python windows installer [here](https://www.python.org/downloads/release/python-375/). 
2. Launch the installer and follow installation instructions on screen.
3. Add Python to system environment path by following [these instructions](https://superuser.com/questions/143119/how-do-i-add-python-to-the-windows-path) so that you can run python from any windows command prompt.

	#### Python Packages
	1. Pip (python installer package). 
		1. Download [get-pip.py](https://bootstrap.pypa.io/get-pip.py) (Right click and click "save as" to download the file).
		2. Open the file in your downloads folder and click the file, this will download pip. It will not give you any confirmation, a window will pop up and disappear. Pip will have loaded after this is complete. If pip did not load successfully you will see an error in the following steps. 

	2. To download the python packages run the following commands from the command prompt (for more info/support, click the names of the packages):
		- [Matplotlib](https://matplotlib.org/users/installing.html#windows)
			```
			python -m pip install matplotlib==3.5.2
			```

		- [NumPy](http://www.numpy.org/)
			```
			python -m pip install numpy==1.21.6
			```

		- [OpenCV](https://pypi.org/project/opencv-python/3.1.0/)
			```
			python -m pip install opencv-python==4.5.5.64
			```

		- [Pyserial](https://github.com/pyserial/pyserial)
			```
			python -m pip install pyserial==3.5
			```

		- [PyQt6](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyqt4)
			```
			python -m pip install pyqt6==6.3
			```

		- [scikit-image](http://scikit-image.org/docs/dev/install.html)
			```
			python -m pip install scikit-image==0.19.2
			```

		- [Scipy](https://www.scipy.org/install.html)
			```
			python -m pip install scipy==1.7.3
			```

		- [Sensapex](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyqt4)
			```
			python -m pip install sensapex==1.22.4
			```
			*Note: you will need to download ump.dll and place it in Lib/site-packages/sensapex*

### 2. Arduino
1. Download the arduino windows installer [here](https://www.arduino.cc/en/Main/Software?).
2. Launch the installer and follow installation instructions on screen.

### 3. Micromanager
1. Download the micromanager windows installer [here](https://micro-manager.org/wiki/Download_Micro-Manager_Latest_Release).
2. Launch the installer and follow installation instructions on screen.
3. Follow [these instructions](https://stackoverflow.com/questions/3701646/how-to-add-to-the-pythonpath-in-windows) to add the following folder to PYTHONPATH vairable:
	- Add "C:\Program Files\Micro-Manager-1.4" to PYTHONPATH variable

### 4. Autoinjector Software 
1. Download or clone this repository by clicking "Clone or Download" button on the top right area of the [Autoinjector Respository](https://github.com/bsbrl/autoinjector/tree/Python3) and extract the files. 

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

### 5. Sensapex SDK
1. Contact [Sensapex](https://www.sensapex.com/products/ump-micromanipulation-system/) and request the "ump.dll" file to use with python. 

2. You will also need to download the file "sensapex.py" from [here](https://github.com/acq4/acq4/blob/2b7a85857b64376d19d2c8658d693b376a5fdbbf/acq4/drivers/sensapex/sensapex.py). 

3. Copy the "ump.dll" and "sensapex.py" files into the folder you downloaded called "motorcontrol" which is in "autoinjector >> motorcontrol".

### 6. Your Camera Driver
Follow the instructions for your camera driver install. In our work we have used the [Hamamatsu Orca Camera](https://www.hamamatsu.com/us/en/product/type/C13440-20CU/index.html) and [Photometrics Cool Snap Dyno PVCam](https://www.photometrics.com/products/ccdcams/coolsnap-dyno.php)

## Running the Application
---------
 
 To run the program normally, click the file "launchapp.py" in the Autoinjector folder. This will launch the GUI and report any errors with hardware. For additional operating instructions see the user manual included with the publication.

## License
-------------
This work is lisenced under the MIT lisence. See LISENCE.txt for additional information.  
