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
5. Sensapex Three/Four axis uMp Micromanipulator 
6. Custom pressure rig

### Software Requirements
Currently, the autoinjector is only available with Windows support. The following libraries are used in the Autoinjector software (see install instructions for how to install). 
1. [Python 3.7+](https://github.com/bsbrl/autoinjector/tree/Python3#1-python)
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
2. [Arduino 1.8+](https://github.com/bsbrl/autoinjector/tree/Python3#2-arduino)
3. [Micromanager 2.0+](https://github.com/bsbrl/autoinjector/tree/Python3#3-micromanager)
4. [Sensapex software](https://github.com/bsbrl/autoinjector/tree/Python3#4-sensapex-sdk)
5. [The Autoinjector software](https://github.com/bsbrl/autoinjector/tree/Python3#5-autoinjector-software)
6. [Your camera driver](https://github.com/bsbrl/autoinjector/tree/Python3#6-your-camera-driver)

## Install Instructions
-------------
Install the following software to operate the Autoinjector. It is recommended to install the software in the order it is listed. Make sure to run every file as administrator (right click, "Run as administrator")! Otherwise, the install may fail. 

### 1. Python
*Note: The following section links to Python 3.7.5, but GUI has been tested and successfully opened in 3.9.13 and 3.10.5.*
1. Download the python windows installer [here](https://www.python.org/downloads/release/python-375/). 
2. Launch the installer and follow installation instructions on screen.
3. Add Python to system environment path by following [these instructions](https://superuser.com/questions/143119/how-do-i-add-python-to-the-windows-path) so that you can run python from any windows command prompt.

	#### Python Packages

	1. To download the python packages run the following commands from the command prompt (for more info/support, click the names of the packages):
		- [Matplotlib](https://matplotlib.org/stable/users/installing/index.html)
			```
			python -m pip install matplotlib==3.5.2
			```

		- [NumPy](http://www.numpy.org/)
			```
			python -m pip install numpy==1.21.6
			```

		- [OpenCV](https://pypi.org/project/opencv-python/4.5.5.64/)
			```
			python -m pip install opencv-python==4.5.5.64
			```

		- [Pyserial](https://pypi.org/project/pyserial/3.5/)
			```
			python -m pip install pyserial==3.5
			```

		- [PyQt6](https://pypi.org/project/PyQt6/)
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

		- [Sensapex](https://pypi.org/project/sensapex/1.22.4/)
			```
			python -m pip install sensapex==1.22.4
			```
			**Note: Installing sensapex from pip will likely be an incomplete installation. You will likely need to follow the guidance in this [GitHub issue](https://github.com/sensapex/sensapex-py/issues/9) to properly install the Sensapex package. In short, you must download the 1.022 binaries from [Sensapex](http://dist.sensapex.com/misc/um-sdk/latest/) and place the "libum.dll" file in the senspex package folder containing "sensapex.py" (i.e. `/python-installation-path/Lib/site-packages/sensapex`)**

### 2. Arduino
1. Download the arduino windows installer [here](https://www.arduino.cc/en/Main/Software?).
2. Launch the installer and follow installation instructions on screen.

### 3. Micromanager
1. Download the micromanager windows installer [here](https://micro-manager.org/wiki/Download_Micro-Manager_Latest_Release).
2. Launch the installer and follow installation instructions on screen.
3. Make sure it is installed at `C://Program Files/Micro-Manager-2.0`

### 4. Autoinjector Software 
1. Download or clone this repository by clicking "Clone or Download" button on the top right area of the [Autoinjector Respository](https://github.com/bsbrl/autoinjector/tree/Python3) and extract the files. 

2. Upload arduino code:
	1. Once the arduino is installed, connect your arduino to your computer via USB.
	2. In the downloaded Autoinjector folder, open the file `/autoinjector/pythonarduino/pythonarduinotriggeropen.ino`
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

### 5. Sensapex sofware
1. Start with pip installing the sensapex package as detailed above. However, pip installing the sensapex package likely resulted in an incomplete installation (a missing piece of software).
2. Follow the guidance in this [GitHub issue](https://github.com/sensapex/sensapex-py/issues/9) to properly install the Sensapex package.
	* To complete the installation, you must download the 1.022 binaries from [Sensapex](http://dist.sensapex.com/misc/um-sdk/latest/) and place the "libum.dll" file in the senspex package folder containing "sensapex.py" (i.e. `/python-installation-path/Lib/site-packages/sensapex`)

### 6. Your Camera Driver
Follow the instructions for your camera driver install. In our work we have used the [Hamamatsu Orca Camera](https://www.hamamatsu.com/us/en/product/type/C13440-20CU/index.html) and [Photometrics Cool Snap Dyno PVCam](https://www.photometrics.com/products/ccdcams/coolsnap-dyno.php)

## Running the Application
---------
 
 To run the program normally, click the file "launchapp.py" in the Autoinjector folder. This will launch the GUI and report any errors with hardware. For additional operating instructions see the user manual included with the publication.

## License
-------------
This work is lisenced under the MIT lisence. See LISENCE.txt for additional information.  
