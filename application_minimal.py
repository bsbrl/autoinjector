
# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from imageprocessing.videocontrolsThread import vidcontrols as vc
from imageprocessing.draw import drawobj
from motorcontrol.altermotorposition import delmotor
from motorcontrol.motorlocationThread import motorpositionThread
from motorcontrol.trajectorythread_minimal import trajectoryimplementor
from pythonarduino.injectioncontrolmod import injection
from resolutiontest.gotoposition import GetPos
import cv2
import serial
import time
import sys
import numpy as np



class ControlWindow(QWidget):
    """ QWidget class to control video stream and capture
    This class controls the GUI of the autoinjector and all subsequent controls including:
    - motor controls and obtaining motor position information
    - injection protocols and triggering 
    - video streaming and acquisition 
    Calling this class will initiate all functions and also present user with GUI (hence bioler plate at bottom of file)
    """

    def __init__(self,cam,brand,val,bins,rot,bits,restest,com):
        QWidget.__init__(self)
        QApplication.setStyle(QStyleFactory.create("Cleanlooks"))
        self.error_msg = QMessageBox()
        self.error_msg.setIcon(QMessageBox.Critical)
        self.error_msg.setWindowTitle("Error")

        # initiate thread to poll position of motors and report error if they are not found
        try:
            self.getposition = motorpositionThread()
            self.getposition.start()
            self.getposition.motorpos.connect(self.showmotorposition)
            self.motorfound = True
        except:
            self.error_msg.setText("Manipulators not detected. Wait 2 minutes then relaunch the app. If this does not work, replug manipulators into computer.")
            self.error_msg.exec_()
            print("Manipulators not detected")
            self.motorfound = False

        # open arduino port and report error if it is not found
        global arduino
        try:
            arduino = serial.Serial(str(com), 9600,timeout=5)
            self.arduinofound = True
            self.com = com
        except:
            self.error_msg.setText("Arduino not detected, make sure you selected the correct com port, plug in and try again.")
            self.error_msg.exec_()
            self.arduinofound = False

        #initiate video stream thread using camera settings
        self.camname = cam
        self.vidctrl = vc(cam,brand,val,bins,rot,bits,restest)
        self.vidctrl.start()
        self.file_selected = 0
        self.restest = restest
        self.GUIsetup()

        #initiate parameters for injection
        self.ninjection = 0 
        self.injectpressurevoltage = 0
        self.pulseduration = 0
        self.edgedetected = False

        self.i = 0 #restest point number
    
    # ---------- Initialize GUI -------------------------------------------------------
    def GUIsetup(self):
        #Create widgets for image display
        self.image_analysis_window_box = QVBoxLayout()
        self.image_analysis_window_box.addWidget(self.vidctrl.image_analysis_window)
        self.image_analysis_window_box.addStretch()
        groupbox_image_analysis_window= QGroupBox('Microscope Stream')
        groupbox_image_analysis_window.setLayout(self.image_analysis_window_box)

        #motor calibration controls
        magnification = QPushButton("Magnification")
        magnification.clicked.connect(self.setmag)
        instruct0 = QLabel("  Step 0  ")
        instruct1 = QLabel("  Step 1  ")
        instruct2 = QLabel("Pipette Angle")
        motorcalib_window_calibutton = QPushButton("Step 1.1", self)
        motorcalib_window_calibutton.clicked.connect(self.showdialog)
        motorcalib_window_calibutton2 = QPushButton("Step 1.2", self)
        motorcalib_window_calibutton2.clicked.connect(self.motorcalib_step2)
        self.motorcalib_window_pipetteangle = QLineEdit(self)
        motorcalib_window_pipetteangle_button = QPushButton("Set Angle", self)
        motorcalib_window_pipetteangle_button.clicked.connect(self.setpipetteangle)
        motorcalib_window = QGridLayout()
        motorcalib_window.addWidget(instruct0,0,0)
        motorcalib_window.addWidget(magnification,0,1,1,2)
        motorcalib_window.addWidget(instruct1,2,0)
        motorcalib_window.addWidget(motorcalib_window_calibutton,2,1)
        motorcalib_window.addWidget(motorcalib_window_calibutton2,2,2)
        motorcalib_window.addWidget(instruct2,3,0)
        motorcalib_window.addWidget(self.motorcalib_window_pipetteangle,3,1)
        motorcalib_window.addWidget(motorcalib_window_pipetteangle_button,3,2)
        groupbox_motorcalib_window = QGroupBox('Motor Calibration')
        groupbox_motorcalib_window.setLayout(motorcalib_window)

        #manual image processing controls
        image_processing_windowmanual_detectedge = QPushButton("Draw Edge")
        image_processing_windowmanual_detectedge.clicked.connect(self.drawedge)
        image_processing_windowmanual = QHBoxLayout()
        image_processing_windowmanual.addWidget(image_processing_windowmanual_detectedge)
        groupbox_image_processing_windowmanual = QGroupBox('Draw Desired Trajectory')
        groupbox_image_processing_windowmanual.setLayout(image_processing_windowmanual)

        #Miscellaneous Controls
        misc = QVBoxLayout()
        misc_hideshape = QPushButton("Hide Shapes")
        misc_hideshape.clicked.connect(self.vidctrl.hideshapes)
        misc_showshape = QPushButton("Show Shapes")
        misc_showshape.clicked.connect(self.vidctrl.showshapes)
        misc.addWidget(misc_showshape)
        misc.addWidget(misc_hideshape)
        groupbox_misc = QGroupBox('Miscellaneous Controls')
        groupbox_misc.setLayout(misc)
        
        #Trajectory planning
        # -*- coding: utf-8 -*-
        self.mu = u"µ"
        self.trajectoryplan = QVBoxLayout()
        self.trajectoryplan_labelaproachdist = QLabel("Approach Distance ("+  self.mu +"m)  ")
        self.trajectoryplan_labeldepth = QLabel("Depth ("+  self.mu +"m)                      ")
        self.trajectoryplan_labelspace = QLabel("Spacing ("+  self.mu +"m)                  ")
        self.trajectoryplan_labelspeed = QLabel("Speed (%)                       ")
        num_cellslabel = QLabel("Number of Cells               ")
        self.trajectoryplan_approach = QLineEdit(self)
        self.trajectoryplan_injectiondepth= QLineEdit(self)
        self.trajectoryplan_spacingbtwn = QLineEdit(self)
        self.trajectoryplan_speed = QLineEdit(self)
        self.num_cells = QLineEdit(self)
        self.trajectoryplan_runbutton = QPushButton("Run Trajectory")
        self.trajectoryplan_runbutton.clicked.connect(self.runalongedgetrajectory)
        self.trajectoryplan_stopbutton = QPushButton("Stop Process")
        self.trajectoryplan_stopbutton.clicked.connect(self.stoptrajectory)
        approach = QHBoxLayout()
        depth = QHBoxLayout()
        space = QHBoxLayout()
        speed = QHBoxLayout()
        num = QHBoxLayout()
        approach.addWidget(self.trajectoryplan_labelaproachdist)
        approach.addWidget(self.trajectoryplan_approach)
        depth.addWidget(self.trajectoryplan_labeldepth)
        depth.addWidget(self.trajectoryplan_injectiondepth)
        space.addWidget(self.trajectoryplan_labelspace)
        space.addWidget(self.trajectoryplan_spacingbtwn)
        speed.addWidget(self.trajectoryplan_labelspeed)
        speed.addWidget(self.trajectoryplan_speed)
        num.addWidget(num_cellslabel)
        num.addWidget(self.num_cells)
        self.trajectoryplan.addLayout(approach)
        self.trajectoryplan.addLayout(depth)
        self.trajectoryplan.addLayout(space)
        self.trajectoryplan.addLayout(speed)
        self.trajectoryplan.addLayout(num)
        groubox_trajectory = QGroupBox('Automated Microinjection Controls')
        groubox_trajectory.setLayout(self.trajectoryplan)

        #automated pressure controls
        #pressure slider
        self.sl = QSlider(Qt.Horizontal)
        self.sl.setMinimum(10)
        self.sl.setMaximum(255)
        self.sl.setValue(10)
        self.sl.setTickPosition(QSlider.TicksBelow)
        self.sl.setTickInterval(30)
        self.sl.valueChanged.connect(self.valuechange)
        self.automatedcontrol_window_left = QVBoxLayout()
        self.automatedcontrol_window_right = QVBoxLayout()
        self.automatedcontrol_window_controls = QHBoxLayout()
        self.automatedcontrol_window_controls_merged = QVBoxLayout()
        compensatpresslabel = QLabel("Compensation Pressure")
        self.compensatpres = QLineEdit(self)
        self.automatedcontrol_window_setvalues = QPushButton("Set Values")
        self.automatedcontrol_window_setvalues.clicked.connect(self.setautomatedparameters)
        self.automatedcontrol_window_left.addWidget(self.sl)
        self.automatedcontrol_window_right.addWidget(self.compensatpres)
        self.automatedcontrol_window_controls.addLayout(self.automatedcontrol_window_left)
        self.automatedcontrol_window_controls.addLayout(self.automatedcontrol_window_right)
        self.automatedcontrol_window_controls_merged.addWidget(compensatpresslabel)
        self.automatedcontrol_window_controls_merged.addLayout(self.automatedcontrol_window_controls)
        self.automatedcontrol_window_bottomwindow = QVBoxLayout()
        self.automatedcontrol_window_bottomwindow.addWidget(self.automatedcontrol_window_setvalues)
        self.automatedcontrol_window_bottomwindow.addWidget(self.trajectoryplan_runbutton)
        self.automatedcontrol_window_bottomwindow.addWidget(self.trajectoryplan_stopbutton)
        self.automatedcontrol_window_controls_merged.addLayout(self.automatedcontrol_window_bottomwindow)
        groupbox_automatedcontrol_window = QGroupBox('Injection Controls')
        groupbox_automatedcontrol_window.setLayout(self.automatedcontrol_window_controls_merged)

        #Motor Status 
        # -*- coding: utf-8 -*-
        self.mu = u"µ"
        self.motorchangeincrementtext = QLabel("Increment (" + self.mu + "m)    ")
        self.motorchangespeedtext = QLabel("    Speed (%)       ")
        self.motorchangeincrement = QLineEdit(self)
        self.motorchangespeed = QLineEdit(self)
        self.motorxpositiontext = QLabel("   X Position     ")
        self.motorypositiontext = QLabel("   Y Position     ")
        self.motorzpositiontext = QLabel("   Z Position     ")
        self.motorxposition = QLineEdit(self)
        self.motoryposition = QLineEdit(self)
        self.motorzposition = QLineEdit(self)
        self.motorxposition.setReadOnly(True)
        self.motoryposition.setReadOnly(True)
        self.motorzposition.setReadOnly(True)
        self.motorxposition_increase = QPushButton("+")
        self.motorxposition_increase.clicked.connect(lambda: self.advancemotor(axis='x',direction='increase'))
        self.motorxposition_decrease = QPushButton("-")
        self.motorxposition_decrease.clicked.connect(lambda: self.advancemotor(axis='x',direction='decrease'))
        self.motoryposition_increase = QPushButton("+")
        self.motoryposition_increase.clicked.connect(lambda: self.advancemotor(axis='y',direction='increase'))
        self.motoryposition_decrease = QPushButton("-")
        self.motoryposition_decrease.clicked.connect(lambda: self.advancemotor(axis='y',direction='decrease'))
        self.motorzposition_increase = QPushButton("+")
        self.motorzposition_increase.clicked.connect(lambda: self.advancemotor(axis='z',direction='increase'))
        self.motorzposition_decrease = QPushButton("-")
        self.motorzposition_decrease.clicked.connect(lambda: self.advancemotor(axis='z',direction='decrease'))
        self.motorchange_inc_param = QHBoxLayout()
        self.motorchange_speed_param = QHBoxLayout()
        self.motorxposition_change_window = QHBoxLayout()
        self.motoryposition_change_window = QHBoxLayout()
        self.motorzposition_change_window = QHBoxLayout()
        self.motorxposition_change_window.addStretch()
        self.motorxposition_increase.setFixedWidth(75)
        self.motorxposition_decrease.setFixedWidth(75)
        self.motoryposition_increase.setFixedWidth(75)
        self.motoryposition_decrease.setFixedWidth(75)
        self.motorzposition_increase.setFixedWidth(75)
        self.motorzposition_decrease.setFixedWidth(75)
        self.motorchange_inc_param.addWidget(self.motorchangeincrementtext)
        self.motorchange_inc_param.addWidget(self.motorchangeincrement)
        self.motorchange_speed_param.addWidget(self.motorchangespeedtext)
        self.motorchange_speed_param.addWidget(self.motorchangespeed)
        self.motorxposition_change_window.addWidget(self.motorxposition_increase)
        self.motorxposition_change_window.addWidget(self.motorxposition_decrease)
        self.motoryposition_change_window.addStretch()
        self.motoryposition_change_window.addWidget(self.motoryposition_increase)
        self.motoryposition_change_window.addWidget(self.motoryposition_decrease)
        self.motorzposition_change_window.addStretch()
        self.motorzposition_change_window.addWidget(self.motorzposition_increase)
        self.motorzposition_change_window.addWidget(self.motorzposition_decrease)
        self.motorposition_change_window = QGridLayout()
        self.motorposition_change_window.addWidget(self.motorxpositiontext,0,0)
        self.motorposition_change_window.addWidget(self.motorxposition,0,1)
        self.motorposition_change_window.addLayout(self.motorxposition_change_window,1,0,1,2)
        self.motorposition_change_window.addWidget(self.motorypositiontext,2,0)
        self.motorposition_change_window.addWidget(self.motoryposition,2,1)
        self.motorposition_change_window.addLayout(self.motoryposition_change_window,3,0,1,2)
        self.motorposition_change_window.addWidget(self.motorzpositiontext,4,0)
        self.motorposition_change_window.addWidget(self.motorzposition,4,1)
        self.motorposition_change_window.addLayout(self.motorzposition_change_window,5,0,1,2)
        self.motorposition_change_window.addLayout(self.motorchange_inc_param,6,0,1,2)
        self.motorposition_change_window.addLayout(self.motorchange_speed_param,7,0,1,2)
        groupbox_motorpanel_window = QGroupBox('Manipulator')
        groupbox_motorpanel_window.setLayout(self.motorposition_change_window)

        #response monitor 
        self.response_monitorgrid= QVBoxLayout()
        self.response_monitor_window = QTextBrowser()
        self.response_monitor_window.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.response_monitorgrid.addWidget(self.response_monitor_window)
        groupbox_response_monitorgrid= QGroupBox('Response Monitor')
        groupbox_response_monitorgrid.setLayout(self.response_monitorgrid)

        #organize main window
        self.mastergrid = QGridLayout()
        self.leftside=QVBoxLayout()
        self.leftside.addWidget(groupbox_motorcalib_window)
        self.leftside.addWidget(groupbox_image_processing_windowmanual)
        self.leftside.addWidget(groupbox_misc)

        if self.restest == "On":
            #resolution test
            self.overrideymotortheta = QLineEdit()
            self.overridepixelsize = QLineEdit()
            go_to_point = QPushButton("Go to res point")
            go_to_point_override = QPushButton("Go to res point override")
            get_current_pos = QPushButton("Record point") #records targeted pos
            calculate_error= QPushButton("Calculate Error") #finds dist between current pos and targeted pos and outputs dist
            go_to_centerpoint = QPushButton("Go to center point")
            go_to_point.clicked.connect(self.go_to_point_func)
            go_to_point_override.clicked.connect(self.go_to_point_func_override)
            get_current_pos.clicked.connect(self.get_current_pos_func)
            calculate_error.clicked.connect(self.calculate_error_func)
            go_to_centerpoint.clicked.connect(self.go_to_centerpoint_func)
            addpoint = QPushButton("Add point")
            addpoint.clicked.connect(self.add_restestpoint)
            subpoint = QPushButton("Sub point")
            subpoint.clicked.connect(self.sub_restestpoint)

            self.leftside.addWidget(self.overrideymotortheta)
            self.leftside.addWidget(self.overridepixelsize)
            self.leftside.addWidget(go_to_point)
            self.leftside.addWidget(go_to_point_override)
            self.leftside.addWidget(get_current_pos)
            self.leftside.addWidget(calculate_error)
            self.leftside.addWidget(addpoint)
            self.leftside.addWidget(subpoint)
            self.leftside.addWidget(go_to_centerpoint)

        self.leftside.addStretch()
        self.rightside=QVBoxLayout()
        self.rightside.addWidget(groupbox_motorpanel_window)
        self.rightside.addWidget(groubox_trajectory)
        self.rightside.addWidget(groupbox_automatedcontrol_window)
        self.rightside.addStretch()

        #Main window details...
        self.setWindowTitle('Autoinjector')
        self.setGeometry(100,100,200,200)
        self.setLayout(self.mastergrid)
        self.show()
        self.setWindowIcon(QIcon('C:\\Users\\taverna\\Desktop\\Autoinjector_Code_cameraselect\\favicon2.png'))
        self.timer = QTimer()  
        self.mastergrid.addLayout(self.leftside,1,0,1,1)
        self.mastergrid.addWidget(groupbox_image_analysis_window,1,1,1,1)
        self.mastergrid.addLayout(self.rightside,1,3,1,1)
        self.mastergrid.addWidget(groupbox_response_monitorgrid, 2,0,1,4)
        self.mastergrid.setContentsMargins(5, 5, 5, 5)

        #print errors on response monitor if manipulator or arduino has an error
        if self.motorfound == False:
            self.response_monitor_window.append(">> Manipulators not detected. Wait 2 minutes then relaunch the app. If this does not work, replug manipulators into computer.")

        if self.arduinofound == False:
            self.response_monitor_window.append(">> Arduino not detected, make sure you selected the correct com port, plug in and try again")
        else:
            self.response_monitor_window.append(">> Arduino connected on port " + str(self.com))

    def setpipetteangle(self):
        self.pipette_angle = self.motorcalib_window_pipetteangle.text()
        self.pipette_angle = float(self.pipette_angle)
        self.thetaz = np.deg2rad(self.pipette_angle)
        print(self.thetaz)

    def valuechange(self):
        self.pressureslidervalue= self.sl.value()
        self.displaypressure = int(self.pressureslidervalue/2.55)
        self.compensatpres.setText('         '+str(self.displaypressure)+'%')

    """
    ----------Calibration Controls -----------------------------------------------------------------
    These functions control the calibration of the manipulators to the camera axes
    """

    def setmag(self):
      items = ("4x", "10x", "20x","40x")
        
      item, ok = QInputDialog.getItem(self, "Select Magnification", 
         "Select Magnification (Assuming 10x objective lens)", items, 0, False)
      self.response_monitor_window.append(">> Magnification set to " +str(item))
      print(self.camname)
      if self.camname == 'Zeis AxioCam':
          print('ugh')
                
      if self.camname == 'HamamatsuHam_DCAM':
          if ok and item:
             if item == "4x":
                self.motorcalibdist = 400000
             elif item == "10x":
                self.motorcalibdist = 160000
             elif item == "20x":
                self.motorcalibdist = 80000
             elif item == "40x":
                self.motorcalibdist = 40000
          
      if self.camname == 'Zeiss AxioCam':
          if ok and item:
             if item == "4x":
                self.motorcalibdist = 200000
             elif item == "10x":
                self.motorcalibdist = 80000
             elif item == "20x":
                self.motorcalibdist = 40000
             elif item == "40x":
                self.motorcalibdist = 20000

      if self.camname == 'Cool Snap Dyno':
          if ok and item:
             if item == "4x":
                self.motorcalibdist = 400000
             elif item == "10x":
                self.motorcalibdist = 320000
             elif item == "20x":
                self.motorcalibdist = 320000
             elif item == "40x":
                self.motorcalibdist = 40000

    def showdialog(self):
        #calibrates motors 
        msg = QMessageBox()
        msg.setWindowIcon(QIcon('C:\\Users\\taverna\\Desktop\\Autoinjector_code\\favicon2.png'))
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Motor Calibration")

        try:
            s = self.motorcalibdist
            msg.setText("Bring the tip into focus and select the tip using Select tip button.")
            msg.setInformativeText("Press OK when complete.")
            msg.buttonClicked.connect(self.motorcalib_step1)
            retval = msg.exec_()

        except:
             self.error_msg.setText("Please select magnification in Calibration window.")
             self.error_msg.exec_()

    def motorcalib_step1(self):
        # gets position of tip if tip is selected. commands motors to move only in y direction
        self.tipposition1 = self.vidctrl.tipcircle
        movey = delmotor('y', 'increase', self.motorcalibdist, 1000,'relative',0)
        movey.start()
            
    def motorcalib_step2(self):
        self.tipposition2 = self.vidctrl.tipcircle
        y1 = self.tipposition1.y()
        y2 = self.tipposition2.y()
        x1 = self.tipposition1.x()
        x2 = self.tipposition2.x()
        ycameraline = abs(y2 - y1)
        xcameraline = abs(x2 - x1)
        self.calculatetheta(xcameraline,ycameraline)


    def calculatetheta(self,xcameraline,ycameraline):
        #solves for the xy theta offset by drawing two lines parellel to camera axes
        ymotorline = np.sqrt((np.square(ycameraline) + np.square(xcameraline)))
        self.ymotortheta = np.arctan(float(xcameraline)/ycameraline)
        self.ymotorthetadeg =np.rad2deg(self.ymotortheta)
        print(self.ymotortheta)
        self.yscale = self.motorcalibdist/ymotorline

        #calculate total FOV of microscope in micromenters
        self.videoheightpixel = int(self.vidctrl.frame.shape[0])
        self.videowidthpixel = int(self.vidctrl.frame.shape[1])
        self.videoheightdist = (self.videoheightpixel)*(self.yscale/1000)
        self.videowidthdist = (self.videowidthpixel)*(self.yscale/1000)
        print("ysclae (nm per pixel" + str(self.yscale))

        self.pixelsize = self.yscale/1000
        print("pixel size = " +str(self.pixelsize))

    """
    ----------Desired Trajectory Control -----------------------------------------------------------------
    This ontrols the detection of the edge of the tissue, and the tip of the pipette
    """   

    def drawedge(self):
        self.vidctrl.showshapes()
        try:
            self.d = drawobj(self.vidctrl.frame)
            self.d.drawedgecoord1 = np.asarray(self.d.drawedgecoord1)
            self.vidctrl.edgearraypointer(self.d.drawedgecoord1)
            print('pointer is')
            print(self.d.drawedgecoord1)
            np.set_printoptions(threshold=np.inf)
            print(self.d.drawedgecoord1)
        except:
            self.error_msg.setText(">> CAM error, is camera plugged in?")
            self.error_msg.exec_()
            self.response_monitor_window.append(">> CAM error, is camera plugged in?")
        
    """
    ---------- Resolution Test Controls   -----------------------------------------------------------------
    These Functions control testing resolution error
    """

    def go_to_point_func(self):
        #get current position of manipulator
        getmotorpos = delmotor('', '', 0, 1000,'getposition_m0',0)
        getmotorpos.start()
        
        time.sleep(0.2)
        print('m0 = ' + str(getmotorpos.m0))
        self.m0 = getmotorpos.m0
        
        #get position of first point in restest grid
        c2x = self.vidctrl.points.drawpointsx
        c2y = self.vidctrl.points.drawpointsy
        self.c2 = (c2x[self.i],c2y[self.i])
        
        #generate commands to go from current point to restest point
        self.c0 = (self.vidctrl.height/2,self.vidctrl.width/2)
        getpos = GetPos(self.c0,self.c2,self.m0,1000,self.ymotortheta,self.thetaz,self.pixelsize)
        print('m1 instructed = ' +  str(getpos.futuremotor))
        self.m1 = getpos.futuremotor

        #use generated commands to move from current point to restest point
        move = delmotor('x', 'increase', getpos.futuremotor, 1000,'absolute',0)
        move.start()

    def go_to_point_func_override(self):
        #rather than using the calibrated ymotor theta and pixel size, these values are input in the gui
        ymotorthetaoverride = float(self.overrideymotortheta.text())
        pixelsizeoverride = float(self.overridepixelsize.text())

        getmotorpos = delmotor('', '', 0, 1000,'getposition_m0',0)
        getmotorpos.start()
        
        time.sleep(0.2)
        print('m0  override = ' + str(getmotorpos.m0))
        self.m0 = getmotorpos.m0
        
        #get position of first point in restest grid
        c2x = self.vidctrl.points.drawpointsx
        c2y = self.vidctrl.points.drawpointsy
        self.c2 = (c2x[self.i],c2y[self.i])
        
        #generate commands to go from current point to restest point
        self.c0 = (self.vidctrl.height/2,self.vidctrl.width/2)
        getpos = GetPos(self.c0,self.c2,self.m0,1000,ymotorthetaoverride,self.thetaz,pixelsizeoverride)
        print('m1 instructed override = ' +  str(getpos.futuremotor))
        self.m1 = getpos.futuremotor

        #use generated commands to move from current point to restest point
        move = delmotor('x', 'increase', getpos.futuremotor, 1000,'absolute',0)
        move.start()

        
    def get_current_pos_func(self):
        #get c1, get m1
        getcurrentmotorm1 = delmotor('', '', 0, 1000,'getposition_m1',0)
        getcurrentmotorm1.start()
        time.sleep(0.4)
        self.m1 = getcurrentmotorm1.m1
        self.c1 = self.vidctrl.positionnow
        print('m1 real =' + str(self.m1))

    def calculate_error_func(self):
        #move to absolute truth position
        getcurrentmotorm2 = delmotor('', '', 0, 1000,'getposition_m2',0)
        getcurrentmotorm2.start()
        time.sleep(0.4)
        self.m2 = getcurrentmotorm2.m2

        self.errorx = abs(int(self.m2[0])-int(self.m1[0]))
        self.errory = abs(int(self.m2[1])-int(self.m1[1]))
        self.errorz = abs(int(self.m2[2])-int(self.m1[2]))
        #.errord = abs(int(self.m2[3])-int(self.m1[3]))

        print('m2 = ' + str(self.m2))
        print('error x,y,z,d in nm = ')
        print(self.errorx)
        print(self.errory)
        print(self.errorz)
        #print(self.errord)

    def go_to_centerpoint_func(self):
        #go back to center point
        middlepos = [12021610, 3279865, 3644745]
        move = delmotor('x', 'increase', middlepos, 1000,'absolute',0)
        move.start()

    def add_restestpoint(self):
        #changes selected point
        self.i = self.i + 1
        print('point vertex = ' + str(self.i))

    def sub_restestpoint(self):
        #changes selected point
        self.i = self.i - 1
        print('point vertex = ' + str(self.i))

    """
    ----------Motor Controls -----------------------------------------------------------------
    These functions control displaying motor position
    All functions call the class delmotor in the altermotorposition.py file
    """

    def showmotorposition(self, motorposition):
        self.motorposition = motorposition
        self.registerpositionx = int(self.motorposition[0])/1000
        self.registerpositiony = int(self.motorposition[1])/1000
        self.registerpositionz = int(self.motorposition[2])/1000
        self.motorxposition.setText(str(self.registerpositionx) +  self.mu +"m")
        self.motoryposition.setText(str(self.registerpositiony) +  self.mu +"m")
        self.motorzposition.setText(str(self.registerpositionz) +  self.mu +"m")

    def advancemotor(self, axis, direction):
        try:
            dist = float(float(self.motorchangeincrement.text())*1000)
            speed = float(self.motorchangespeed.text())
            move = delmotor(axis, direction, dist, speed,'relative',0)
            move.start()
        except:
             self.error_msg.setText("Please enter an increment and speed in the manipulator window.")
             self.error_msg.exec_()


    """
    ----------Automated Microinjection Controls  -----------------------------------------------------------------
    These functions control the trajectory and pressure controls of the GUI
    """

    def setautomatedparameters(self):
        try:
            self.compensationpressureval = self.pressureslidervalue
            self.compensationpressureval =str(self.compensationpressureval)
            self.ncell=self.num_cells.text()
            self.approachdist = self.trajectoryplan_approach.text()
            self.deptintissue = self.trajectoryplan_injectiondepth.text()
            self.stepsize = self.trajectoryplan_spacingbtwn.text()
            self.motorspeed = self.trajectoryplan_speed.text()
            self.injectpressurevoltage = self.compensationpressureval
            self.response_monitor_window.append(">> Values set")
            self.injector_compensate = injection(arduino,self.compensationpressureval, 0,self.injectpressurevoltage,0,'bp')
            self.injector_compensate.start()

        except:
             self.error_msg.setText("Error, did you enter all parameters? Is the arduino plugged in?")
             self.error_msg.exec_()                

        
    def runalongedgetrajectory(self):
        #try:
            #get values from GUI
        currentpos = self.vidctrl.positionnow 
        approach = (int(float(self.approachdist)*1000)) #convert microns to nm
        depth = (int(float(self.trajectoryplan_injectiondepth.text()))*1000)
        depthintissue = depth
        space = int(float(self.trajectoryplan_spacingbtwn.text()))
        self.speed = (int((self.trajectoryplan_speed.text()))*10)
        spacing = space

        self.trajimplement = trajectoryimplementor(self.ymotortheta, self.thetaz, currentpos, self.pixelsize, approach, depthintissue, spacing, self.d.drawedgecoord1, self.ncell, self.speed)
        self.trajimplement.start()
        self.trajimplement.finished.connect(self.updateresponse)

        #except:
        #    self.error_msg.setText("Please complete calibration, enter all parameters, and select tip of pipette.")
        #    self.error_msg.exec_()

    def updateresponse(self):
        self.response_monitor_window.append(">> Number of injections =" + str(self.trajimplement.statusnumber))

    def stoptrajectory(self):
        try:
            self.trajimplement.stopprocess()
        except:
            self.error_msg.setText("You have to start the trajectory in order to be able to stop it...")
            self.error_msg.exec_()

    def closeEvent(self, event):
        self.close()
        sip.destroyonexit(True)