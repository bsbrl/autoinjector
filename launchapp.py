#!/usr/bin/python
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
from application_minimal import ControlWindow

class camerasetting(QWidget):
	def __init__(self):
		QWidget.__init__(self)
		self.initUI()

	def initUI(self):
		#set layout of Camera setting User interface
		layout1 = QHBoxLayout()
		cameralabel = QLabel("Camera")
		camera = QComboBox(self)
		camera.addItem("Select a Camera")
		camera.addItem("Tis CAM - not tested")
		camera.addItem("Hamamatsu Orca DCAM")
		camera.addItem("Zeiss Axiocam")
		camera.addItem("PVCam")
		camera.activated[str].connect(self.updatecamera)
		layout1.addWidget(cameralabel)
		layout1.addWidget(camera)
		groupboxlayout1 = QGroupBox("Camera Selection")
		groupboxlayout1.setLayout(layout1)

		self.layout2 = QGridLayout()
		devicenamelabel = QLabel("Device Name")
		brandlabel = QLabel("Brand")
		devicevaluelabel = QLabel("Device Value")
		binslabel = QLabel("Binning")
		bitlabel = QLabel("Bits")
		rotatelabel = QLabel("Rotate (CW)")
		self.devicename1 = QLineEdit(self)
		self.brand1 = QLineEdit(self)
		self.devicevalue1 = QLineEdit(self)
		bits = QComboBox(self)
		bits.addItem("4")
		bits.addItem("8")
		bits.addItem("16")
		bits.addItem("32")
		bits.activated[str].connect(self.updatebits)
		bins = QComboBox(self)
		bins.addItem("1x1")
		bins.addItem("2x2")
		bins.addItem("4x4")
		bins.activated[str].connect(self.updatebins)
		rotate = QComboBox(self)
		rotate.addItem("0")
		rotate.addItem("90")
		rotate.addItem("180")
		rotate.addItem("270")
		rotate.activated[str].connect(self.updaterotate)

		self.layout2.addWidget(devicenamelabel, 0,0,1,1)
		self.layout2.addWidget(brandlabel, 1,0,1,1)
		self.layout2.addWidget(devicevaluelabel, 2,0,1,1)
		self.layout2.addWidget(binslabel, 4,0,1,1)
		self.layout2.addWidget(bitlabel, 3,0,1,1)
		self.layout2.addWidget(rotatelabel, 5,0,1,1)
		self.layout2.addWidget(self.devicename1, 0,1,1,1)
		self.layout2.addWidget(self.brand1, 1,1,1,1)
		self.layout2.addWidget(self.devicevalue1, 2,1,1,1)
		self.layout2.addWidget(bins, 4,1,1,1)
		self.layout2.addWidget(bits, 3,1,1,1)
		self.layout2.addWidget(rotate, 5,1,1,1)
		groupboxlayout2 = QGroupBox('Custom Settings')
		groupboxlayout2.setLayout(self.layout2)

		self.layout3 = QHBoxLayout()
		restestlabel = QLabel("Resolution Test?")
		restest = QComboBox(self)
		restest.addItem("Select")
		restest.addItem("On")
		restest.addItem("Off")
		restest.activated[str].connect(self.updaterestest)

		self.layout3.addWidget(restestlabel)
		self.layout3.addWidget(restest)
		groupboxlayout3 = QGroupBox('Resolution Test')
		groupboxlayout3.setLayout(self.layout3)


		QApplication.setStyle(QStyleFactory.create("Cleanlooks"))
		mainlayout = QVBoxLayout()
		saveexitbutton = QPushButton("Save and Exit")
		saveexitbutton.clicked.connect(self.close1)
		#mainlayout.addWidget(groupboxlayout0)
		mainlayout.addWidget(groupboxlayout1)
		mainlayout.addWidget(groupboxlayout2)
		mainlayout.addWidget(groupboxlayout3)
		mainlayout.addWidget(saveexitbutton)
		self.setWindowTitle('Settings')
		self.setGeometry(550,200,250,100)
		self.setLayout(mainlayout)
		self.show()

	def updatecamera(self,text):
		if text == 'PVCam':
			self.devicename = 'Cool Snap Dyno'
			self.brand = 'PVCAM'
			self.devicevalue = 'Camera-1'
			self.bins = "none"
			self.rotate = 180
			self.bits = 16                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     


		if text == 'Hamamatsu Orca DCAM':
			self.devicename = 'HamamatsuHam_DCAM'
			self.brand = 'HamamatsuHam'
			self.devicevalue = 'HamamatsuHam_DCAM'
			self.bins = "2x2"
			self.rotate = 270
			self.bits = 16


		if text == "Tis Cam":
			self.devicename = 'TIS_DCAM'
			self.brand = 'TIScam'
			self.devicevalue = 'TIS_DCAM'
			self.bins = "none";
			self.rotate = 270
			self.bits = 8


		if text == 'Zeiss Axiocam':
			self.devicename = 'Zeiss AxioCam'
			self.brand = 'AxioCam'
			self.devicevalue = 'Zeiss AxioCam'
			self.bins = "none"
			self.rotate = 270
			self.bits = 16                   


	def updatebits(self,text):
		self.bits = int(text)
		print(self.bits)

	def updatebins(self,text):
		self.bins = text
		print(self.bins)

	def updaterotate(self,text):
		self.rotate = int(text)
		print(self.rotate)

	def updaterestest(self,text):
		self.restest = text
		print(self.restest)

	def close1(self):
		self.close()
		x = ControlWindow(self.devicename,self.brand,self.devicevalue,self.bins,self.rotate,self.bits, self.restest)
		x.show()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    app.setApplicationName('MyWindow')
    main = camerasetting()
    main.show()
    sys.exit(app.exec_())
           



