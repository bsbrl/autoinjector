from PyQt4.QtCore import *
from PyQt4.QtGui import *
import cv2
import numpy as np
import time
import MMCorePy
#for tracking tip
import os
import time
from imutils import face_utils
from restestgrid import ResTest


import os
import sys
MM_PATH = os.path.join('C:', os.path.sep, 'Program Files',
'Micro-Manager-1.4')
sys.path.append(MM_PATH)
os.environ['PATH'] = MM_PATH + ';' + os.environ['PATH']


class vidcontrols(QThread):
    #vidout = pyqtSignal()

    def __init__(self,cam,brand,val,bins,rot,bits,restest):
        #defines camera settings
        self.cam = cam
        self.brand = brand
        self.val = val
        self.bins = bins
        self.rot = int(rot)
        self.bits = int(bits)
        self.restest = restest

        
        #initiates stream of video 
        QThread.__init__(self)
        self.image_analysis_window = QLabel() #creates place to put stream of vid
        self.CAMsetup() #set up camera
        self.refreshbutton = QPushButton("Refresh Video")
        self.streamtranslate() #stream video
        self.keeptracking = False #initialize variable for later
        self.vidnum = 0 #count number of recordings
        self.gotopos = False
        self.hideshapecommand = False

    # ---------------------- Camera Setup ------------------------------------------
    def CAMsetup(self):
        try:
            self.cap = MMCorePy.CMMCore()
            self.cap.loadDevice(self.cam,self.brand,self.val)
            self.cap.initializeAllDevices()
            self.cap.setCameraDevice(self.cam)
            if self.bins != "none":
                self.cap.setProperty(self.cam, "Binning", self.bins)
            self.cap.startContinuousSequenceAcquisition(1)

            self.timer = QTimer()
            self.timer.timeout.connect(self.streamtranslate)
            self.timer.start(30)
            self.startcap = 0
            self.endcap = 0
            self.calib = 0
            
        except:
            self.image_analysis_window.setText('CAMERA ERROR. Verify camera is detected in Device Manager, correct camera settings are applied, and restart program')

    def streamtranslate(self):
        #this function controls the streaming video 

        #if video is streaming
        if self.cap.getRemainingImageCount() > 0:
            self.frame = self.cap.getLastImage()

            if self.cam == 'HamamatsuHam_DCAM': #convert to 8bit
                self.frame = (self.frame/256).astype('uint8')
                self.scalefactor = 1.3
            if self.cam == 'Zeiss AxioCam':
                self.frame = (self.frame/65536).astype('uint8')
                self.scalefactor = 1.1
            if self.cam == 'Cool Snap Dyno':
                self.frame = (self.frame/256).astype('uint8')
                self.scalefactor = 2.4

            if self.rot > 0: #rotate 
                rows,cols = self.frame.shape 
                M = cv2.getRotationMatrix2D((cols/2,rows/2),self.rot,1)
                self.frame = cv2.warpAffine(self.frame,M,(cols,rows))

            self.width = int(self.frame.shape[0])
            self.height = int(self.frame.shape[1])


            #resolution testing grid
            if self.restest == "On":
                try:
                    #cv2.circle(self.frame, (self.width/2, self.height/2), 3, 255, -1)
                    for i in xrange(0,len(self.points.drawpointsx)):
                        cv2.circle(self.frame, (self.points.drawpointsx[i], self.points.drawpointsy[i]), 1, 255, -1)
                except:
                    self.points = ResTest()
                    self.points.makePoints(self.height,self.width)


            #Look to see if correlation tip tracking on, track if it is

            try:
                if self.hideshapecommand == False:
                    cv2.circle(self.frame, (self.self.pixelclicked.x(), self.self.pixelclicked.y()), 1, 255, -1)
            except:
                s = 1

            
            try: #draws position clicked
                cv2.circle(self.frame,(int(self.scalefactor*self.pixelclicked.x()),int(self.scalefactor*self.pixelclicked.y())), 3,255, -1)

            except:
                s = 1

            if self.hideshapecommand == False:
            	try:#Look to see if edge coordinates exist, display them if they do, otherwise display vid
            		cv2.polylines(self.frame, [self.edgearray], False, (255,255,255),1)
            	except:
            		s=1
            		
            if self.startcap == 1: #video capture settings
                self.out.write(self.frame)
                if self.endcap == 1:
                    self.out.release()
                    self.startcap = 0
            
            #display frame
            self.image = QImage(self.frame, self.frame.shape[1], self.frame.shape[0], self.frame.strides[0], QImage.Format_Indexed8)
            self.image_analysis_window.setPixmap(QPixmap.fromImage(self.image.scaledToWidth((self.frame.shape[1]/self.scalefactor),Qt.SmoothTransformation)))
            self.image_analysis_window.setFixedSize((self.frame.shape[1]/self.scalefactor),(self.frame.shape[0]/self.scalefactor))
            self.image_analysis_window.mousePressEvent = self.getPos

    #-------------------------- Motor calibration command
    def calcymotortheta(self,p1,p2):
        self.position1 = p1
        self.position2 = p2

    def getPos(self , QMouseEvent):
        #get position of click in qpixmap
        self.pixelclicked = (QMouseEvent.pos())
        self.tipcircle = (self.pixelclicked*self.scalefactor)
        x = self.tipcircle.x()
        y = self.tipcircle.y()
        self.positionnow = (x,y)
        print(self.positionnow)

    def showshapes(self):
        self.hideshapecommand = False

    def hideshapes(self):
        #hides the shapes from image when trajectory is in progress as triggered in runalongedgetrajectory
        self.hideshapecommand = True

    #------------------------ Edge/Tip detection functions----------------------------------
    def selecttip_corr(self):
        self.tiptrack = corr(self.frame)
        self.tiptrack.GUItoSelect()
        try:
            (xmin, ymin, xmax, ymax) = self.tiptrack.selection
        except:
            print('Error in dlib tracking function')

    def drawinwindow(self):
        #puts image frame in GUI
        self.image = QImage(self.frame, self.frame.shape[1], self.frame.shape[0], self.frame.strides[0], QImage.Format_Indexed8)
        self.image_analysis_window.setPixmap(QPixmap.fromImage(self.image.scaledToWidth(800,Qt.SmoothTransformation)))

    def edgearraypointer(self,edgearray):
        self.edgearray = edgearray

    def displaytip(self,tipx,tipy):
        #draws coordinates output from tipdetector
        self.tipx = tipx
        self.tipy = tipy

    #---------------------- Video Capture Functions ------------------------------------------
    def startcapture(self):
        #get working directory
        date = time.strftime("%d_%m_%Y")
        timename = "time_" + time.strftime("%H_%M_%S")
        dir1 = os.getcwd()

        try:
            os.mkdir('Video Data')
        except:
            print('dirmade')
        
        os.chdir('Video Data')

        try:
            os.getcwd()
            os.mkdir(date)
        except:
            print('directory = ' + str(date))
            
        #make outputfile
        self.images_list =[]
        self.fourcc = cv2.VideoWriter_fourcc('M','S','V','C')
        os.chdir(date)
        self.outputfile= str(timename) + '.avi'
        self.out = cv2.VideoWriter(self.outputfile, -1, 12, (self.height,self.width))
        os.chdir(dir1)
        
        self.streamtranslate()
        self.vidstatus = "Video Capture Started"
        self.startcap = 1
        self.endcap = 0

    def endcapture(self):
        self.endcap = 1
        self.vidstatus = "Video Capture Ended; file written to   " + self.outputfile
    




