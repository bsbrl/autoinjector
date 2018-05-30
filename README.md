## Autoinjector

The autoinjector is an automated computer vision guided platform to serially inject tissue with user parameter selection along a specified trajectory using a 3-axis micromanipulator. The user can control the following parameters:

- Number of cells to inject
- Number of injections/cell
- Injection pulse duration
- Injection pressure 
- Depth into tissue to inject
- Spacing between points along trajectory
- Compensation pressure
- Speed of manipulators

Additionally, the user can record videos from the GUI. 

## Software 
Currently, the autoinjector is only available with Windows support. Future work will focus on extending to Ubuntu, and Mac OS X. The following software and libraries are  included in the install instructions.
- Arduino
- Python 2.7.12 
	- Dlib 18.17.100 +
	- Matplotlib 2.0.0 +
	- MMCorepy (Micromanager API)
	- Numpy 1.12.0 +
	- OpenCV 3.1.0 +
	- Pyserial 
	- PyQt 4.11.14 +
	- scikit-image 0.13.0 +
	- Scipy 0.19.0 +
- Micromanager 1.4.22 +


## Hardware requirements 
A complete list of available cameras can be found at micromanager's device support (https://micro-manager.org/wiki/Device_Support). Manipulator support exists for Sensapex manipulators only. However, if the manipulators have available SDK, custom API can be made using Python's ctypes. Contact G. Shull for additional support for adapting SDKs for python use. 
- Computer
- Arduino Uno
- Microscope (brightfield, phase contrast, or DIC)
- Microscope camera
- Manipulator 
- Custom pressure rig

## Installation

1. Download or clone this repository by clicking "Clone or Download" and extract the files. 

2. Right click the batch file titled "SETUP" and click edit. This will open the notepad editor. Replace the path C:\downloads\Autoinjector\Setup Downloads with the path that contains your Setup Downloads folder. You can obtain this path by opening the folder, right clicking the path title, and clicking "copy address as text". Once you have replaced the path, save the file and close notepad. 

3. Right click the file "SETUP" and click "Run as administrator" to run the installation of arduino,python, external libraries, and micromanager. NOTE it does not matter where you save the arduino, python, or micromanager directory, but make sure you remember the micromanager directory location. It is also helpful to click the create shortcut option in the micromanager GUI.

4. Launch the micromanager program and follow instructions https://micro-manager.org/wiki/Micro-Manager_Configuration_Guide to create a configuration file for your camera. 


## Running the Application

 To run the program click the file "application.py" in the main directory. This will launch the GUI and report any errors with hardware.

## License

This work is lisenced under the MIT lisence. See LISENCE.txt for additional information.  
