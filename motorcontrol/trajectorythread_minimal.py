from PyQt4.QtCore import *
from PyQt4.QtGui import *
import os, sys, time
from motorcontrol_thread import motorcontroller as mc
import numpy as np



class trajectoryimplementor(QThread):
    """
    This class creates and calls trajectories to the manipulator. The inputs are as follows:
    xmotortheta = theta offset in radians between x of manipulator and x of camera
                    (generated in x calibration step 2)
    thetaz = angle beetween x axis of manipulator and x axis of camera frame
    currentpos = array of (x,y) coordinate of current position of tip of pipette
                 (generated from vidcontrol tipcircle var)
    pixelsize = size of pixel in microns (integer input from GUI)
    approachdist = the distance from the edge of the tissue that the pipette pulls out after each injection  (taken from user input in GUI)
    depthintissue = the depth of injection (taken from user input in GUI)
    spacingbtwn = numerical spacing between injection sites in nanometers
                    (taken from user input in GUI)
    edgecoord = list of coordinates of desired points in the imaging plane to move the pipette
                (generates from draw edge coord or automatic edge detection function)
    ncells = number of cells to inject (taken from user input in GUI)
    speed = speed of manipulator entry
    offset = offset
    """

    def __init__(self, xytheta, thetaz, currentpos, pixelsize, approachdist, depthintissue, spacingbtwn, edgecoord, ncells, speed,offset):
        QThread.__init__(self)
        self.stopsignal = False
        self.xthetarad = xytheta
        self.thetaz = thetaz
        self.currentposition = currentpos
        self.pixelsize = pixelsize
        self.approachdist = approachdist
        self.depthintissue = depthintissue
        self.spacingbtwn = (spacingbtwn/(self.pixelsize))
        self.edgecoords = edgecoord
        self.numbercells = ncells
        self.speed = speed
        self.offset1 = offset
        
    def __del__(self):
        self.wait()

    def run(self):
        self.implement_traj()


    def implement_traj(self):

        trajectoryarray = []
        for i in range(1,int(self.numbercells)):
            self.statusnumber = i
            self.motorfinished = False
            print("Injection number = ")
            print(i)

            if self.stopsignal == True:
                break

            if i == 1:
                x0 = self.currentposition[0]
                y0 = self.currentposition[1]
                arrayf = self.edgecoords[int(i*self.spacingbtwn)]
                xf = arrayf[0]
                yf = arrayf[1] 

            if i  > 1:
                arrayf = self.edgecoords[int(i*self.spacingbtwn)]
                print(int(i*self.spacingbtwn))
                xf = arrayf[0]
                yf = arrayf[1]
                array1 = self.edgecoords[(int((i-1)*self.spacingbtwn))]
                x0 = array1[0]
                y0 = array1[1]

            x = xf - x0
            y = yf - y0
            print('x, y = ' + str(x) +',' +str(y))
            a = np.array([[-np.cos(self.xthetarad), -np.sin(self.xthetarad)], [-np.sin(self.xthetarad), -np.cos(self.xthetarad)]])
            b = np.array ((x,y))
            print('a =' + str(a))
            print('b = ' + str(b))

            #corrects for b offset at 20x magnifcation
            if b[0] <= 0:
                self.offset = self.offset1[0]
            else:
                self.offset = self.offset1[1]

            print("offset = " + str(self.offset))

            manipulator = np.linalg.solve(a, b)
            print('dx,dy = ' + str(manipulator))
            manipulator_motorscaled = manipulator*self.pixelsize*1000 #(in nanometers)
            print('manipulator_motorscaled =' + str(manipulator_motorscaled))

            trajectoryarray.append([manipulator_motorscaled])
            k = trajectoryarray[(i-1)]
            print('k = ' + str(k))
            zcorrected = (k[0][0]/(np.cos(self.thetaz)))
            print('zcorrected =' + str(zcorrected))  
            zcorrected = zcorrected-self.offset
            zdrift = -zcorrected*(np.cos(self.thetaz))

            self.motorcalib3 = mc(zdrift, zcorrected, k[0][1], self.approachdist, self.depthintissue, self.speed)
            self.connect(self.motorcalib3, SIGNAL("finished()"),self.turnsignal)
            self.motorcalib3.start()

            while self.motorfinished == False:
                time.sleep(0.1)
                
        print(trajectoryarray)


    def turnsignal(self):
        #switches for loop to calculate and send next command to manipulator
        print('Injection complete')
        self.motorfinished = True

    def stopprocess(self):
        self.stopsignal = True
