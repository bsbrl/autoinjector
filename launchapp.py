#!/usr/bin/python
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import QIcon
import sys
from application_minimal import ControlWindow
import numpy as np

class camerasetting(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowIcon(QIcon('favicon.png'))
        self.initUI()
        self.custom = False

    def initUI(self):
        #set layout of Camera setting User interface
        layout1 = QHBoxLayout()
        cameralabel = QLabel("Camera")
        camera = QComboBox(self)
        camera.addItem("Select")
        camera.addItem("Hamamatsu Orca DCAM")
        camera.addItem("Zeiss Axiocam")
        camera.addItem("PVCam")
        camera.addItem("Custom")
        camera.textActivated[str].connect(self.updatecamera)
        layout1.addWidget(cameralabel)
        layout1.addWidget(camera)
        groupboxlayout1 = QGroupBox("Camera Selection")
        groupboxlayout1.setLayout(layout1)

        self.layout3 = QHBoxLayout()
        restestlabel = QLabel("Resolution Test?")
        restest = QComboBox(self)
        restest.addItem("Select")
        restest.addItem("On")
        restest.addItem("Off")
        restest.textActivated[str].connect(self.updaterestest)
        self.layout3.addWidget(restestlabel)
        self.layout3.addWidget(restest)
        groupboxlayout3 = QGroupBox('Resolution Test')
        groupboxlayout3.setLayout(self.layout3)

        self.layout4 = QHBoxLayout()
        comlabel = QLabel("Arduino Com Port")
        com = QComboBox(self)
        com.addItem("Select")
        com.addItem("com1")
        com.addItem("com2")
        com.addItem("com3")
        com.addItem("com4")
        com.addItem("com5")
        com.addItem("com6")
        com.addItem("com7")
        com.addItem("com8")
        com.addItem("com9")
        com.addItem("com10")
        com.addItem("com11")
        com.textActivated[str].connect(self.updatecom)
        self.layout4.addWidget(comlabel)
        self.layout4.addWidget(com)
        groupboxlayout4 = QGroupBox('Arduino Com Port Selection')
        groupboxlayout4.setLayout(self.layout4)

        QApplication.setStyle(QStyleFactory.create("Fusion"))
        mainlayout = QVBoxLayout()
        saveexitbutton = QPushButton("Save and Exit")
        saveexitbutton.clicked.connect(self.close1)
        mainlayout.addWidget(groupboxlayout1)
        mainlayout.addWidget(groupboxlayout4)
        mainlayout.addWidget(groupboxlayout3)
        #mainlayout.addWidget(groupboxlayout2)
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
            bits = 8  
            self.fourtyxmagcalibdist = 40000 
            self.scalefactor = 2.4                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                


        if text == 'Hamamatsu Orca DCAM':
            self.devicename = 'HamamatsuHam_DCAM'
            self.brand = 'HamamatsuHam'
            self.devicevalue = 'HamamatsuHam_DCAM'
            self.bins = "2x2"
            self.rotate = 180
            bits = 8
            self.fourtyxmagcalibdist = 40000 
            self.scalefactor = 1.3

        if text == 'Zeiss Axiocam':
            self.devicename = 'Zeiss AxioCam'
            self.brand = 'AxioCam'
            self.devicevalue = 'Zeiss AxioCam'
            self.bins = "none"
            self.rotate = 270
            bits = 16
            self.fourtyxmagcalibdist = 30000 
            self.scalefactor = 1.5

        if text == 'Custom':
            #do popup
            self.customvals = CustomCam()
            self.customvals.show() 
            self.custom = True

        self.imagevals = np.power(2, bits)

    def updaterestest(self,text):
        self.restest = text

    def updatecom(self,text):
        self.com = text

    def close1(self):
        try:
            if self.custom == True:
                self.devicename = self.customvals.devicename
                self.brand = self.customvals.brand
                self.devicevalue = self.customvals.devicevalue
                self.bins = self.customvals.bins
                self.rotate = int(self.customvals.rotate)
                bits = int(self.customvals.bits)
                self.imagevals = np.power(2, bits)
                self.scalefactor = float(self.customvals.scalefactor)
                self.fourtyxmagcalibdist = int(self.customvals.fourtyxmagcalib)
            self.close()
            x = ControlWindow(self.devicename,self.brand,self.devicevalue,self.bins,self.rotate,self.imagevals, self.scalefactor, self.restest,self.com, self.fourtyxmagcalibdist)
            x.show()
            print(self.devicename +","+ self.brand + ","+self.devicevalue + ","+self.bins + ","+str(self.rotate) +","+ str(self.imagevals) +","+ str(self.scalefactor) + ","+str(self.fourtyxmagcalibdist))
            
        except:
            error_msg = QMessageBox()
            error_msg.setIcon(QMessageBox.Icon.Critical)
            error_msg.setWindowTitle("Error")
            error_msg.setText("All options were not selected. Please choose all options and try again. \n Python error = \n" + str(sys.exc_info()[1]))
            error_msg.exec()
        

class CustomCam(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowIcon(QIcon('favicon.png'))
        self.showbox()

    def showbox(self):
        self.layout2 = QGridLayout()
        devicenamelabel = QLabel("Device Name")
        brandlabel = QLabel("Brand")
        devicevaluelabel = QLabel("Device Value")
        binslabel = QLabel("Binning")
        bitlabel = QLabel("Bits")
        rotatelabel = QLabel("Rotate (CW)")
        scalfaclabel = QLabel("Scale Factor")
        calibdistlabel = QLabel("40x calibration dist")
        self.devicename1 = QLineEdit(self)
        self.brand1 = QLineEdit(self)
        self.devicevalue1 = QLineEdit(self)
        self.scalefactor1 = QLineEdit(self)
        self.fourtyxmagcalibdist1 = QLineEdit(self)
        bits = QComboBox(self)
        bits.addItem("Select")
        bits.addItem("4")
        bits.addItem("8")
        bits.addItem("16")
        bits.addItem("32")
        bits.textActivated[str].connect(self.updatebits)
        bins = QComboBox(self)
        bins.addItem("Select")
        bins.addItem("1x1")
        bins.addItem("2x2")
        bins.addItem("4x4")
        bins.textActivated[str].connect(self.updatebins)
        rotate = QComboBox(self)
        rotate.addItem("Select")
        rotate.addItem("0")
        rotate.addItem("90")
        rotate.addItem("180")
        rotate.addItem("270")
        rotate.textActivated[str].connect(self.updaterotate)
        self.layout2.addWidget(devicenamelabel, 0,0,1,1)
        self.layout2.addWidget(brandlabel, 1,0,1,1)
        self.layout2.addWidget(devicevaluelabel, 2,0,1,1)
        self.layout2.addWidget(binslabel, 4,0,1,1)
        self.layout2.addWidget(bitlabel, 3,0,1,1)
        self.layout2.addWidget(rotatelabel, 5,0,1,1)
        self.layout2.addWidget(scalfaclabel, 6,0,1,1)
        self.layout2.addWidget(calibdistlabel, 7,0,1,1)
        self.layout2.addWidget(self.devicename1, 0,1,1,1)
        self.layout2.addWidget(self.brand1, 1,1,1,1)
        self.layout2.addWidget(self.devicevalue1, 2,1,1,1)
        self.layout2.addWidget(bins, 4,1,1,1)
        self.layout2.addWidget(bits, 3,1,1,1)
        self.layout2.addWidget(rotate, 5,1,1,1)
        self.layout2.addWidget(self.scalefactor1, 6, 1,1,1)
        self.layout2.addWidget(self.fourtyxmagcalibdist1, 7,1,1,1)
        groupboxlayout2 = QGroupBox('Custom Settings')
        groupboxlayout2.setLayout(self.layout2)

        QApplication.setStyle(QStyleFactory.create("Fusion"))
        mainlayout = QVBoxLayout()
        saveexitbutton = QPushButton("Save and Exit")
        saveexitbutton.clicked.connect(self.closecustom)
        mainlayout.addWidget(groupboxlayout2)
        mainlayout.addWidget(saveexitbutton)
        self.setWindowTitle('Settings')
        self.setGeometry(550,200,250,100)
        self.setLayout(mainlayout)
        self.show()

    def updatebits(self,text):
        self.bits = int(text)
        print(self.bits)

    def updatebins(self,text):
        self.bins = str(text)
        print(self.bins)

    def updaterotate(self,text):
        self.rotate = int(text)
        print(self.rotate)

    def closecustom(self):
        self.scalefactor = self.scalefactor1.text()
        self.fourtyxmagcalib = self.fourtyxmagcalibdist1.text()
        self.devicename = str(self.devicename1.text())
        self.brand = str(self.brand1.text())
        self.devicevalue = str(self.devicevalue1.text())
        self.close()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    app.setApplicationName('MyWindow')
    main = camerasetting()
    main.show()
    sys.exit(app.exec())
           



