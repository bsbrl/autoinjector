# Autoinjector

The autoinjector is an automated computer vision guided platform to serially inject tissue with user parameter selection along a specified trajectory using a 3-axis micromanipulator. This read me takes you through the system requirements, install instructions, operating instructions, and how to customize the code based on different cameras. For a complete description of the device see the Autoinjector paper and supplementary materials. 

1. [System Requirements](https://github.com/ogshull/Autoinjector-#system-requirements)
	- [Hardware Requirements](https://github.com/ogshull/Autoinjector-#hardware-requirements)
	- [Software Requirements](https://github.com/ogshull/Autoinjector-#software-requirements)
2. [Install Instructions](https://github.com/ogshull/Autoinjector-#install-instructions)
	- Install Python 2.7.13
	- Install Arduino
	- Install Micromanager
	- Install Sensapex SDK
	- Install Python packages 

It is recommended to start in order. 

## System requirements 
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

## Install Instructions

### Python
1. Download the python windows installer [here](https://www.python.org/downloads/release/python-2713/). 
2. Launch the installer and follow installation instructions on screen.

### Arduino
1. Download the arduino windows installer [here](https://www.arduino.cc/en/Main/Software?).
2. Launch the installer and follow installation instructions on screen.

### Micromanager
1. Download the micromanager windows installer [here](https://micro-manager.org/wiki/Download_Micro-Manager_Latest_Release).
2. Launch the installer and follow installation instructions on screen.

### Sensapex SDK
1.... Need to figure out how to distrubute SDK

### Autoinjector Software 
1. Download or clone this repository by clicking "Clone or Download" button on the topright area of the [Autoinjector Respository](https://github.com/ogshull/autoinjector-) and extract the files. 

2. Right click the batch file titled "SETUP" and click edit. This will open the notepad editor. Replace the path C:\downloads\Autoinjector\Setup Downloads with the path that contains your Setup Downloads folder. You can obtain this path by opening the folder, right clicking the path title, and clicking "copy address as text". Once you have replaced the path, save the file and close notepad. 

3. Right click the file "SETUP" and click "Run as administrator" to run the installation of arduino,python, external libraries, and micromanager. NOTE it does not matter where you save the arduino, python, or micromanager directory, but make sure you remember the micromanager directory location. It is also helpful to click the create shortcut option in the micromanager GUI.

4. Launch the micromanager program and follow instructions https://micro-manager.org/wiki/Micro-Manager_Configuration_Guide to create a configuration file for your camera. 


## Running the Application

 To run the program click the file "launchapp.py" in the main directory. This will launch the GUI and report any errors with hardware.

## License

This work is lisenced under the MIT lisence. See LISENCE.txt for additional information.  
