from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import os, sys, time
from .motorcontrol_thread import motorcontroller as mc
from .motorcontrol_thread import motorcontroller_improved as mci
import numpy as np
import traceback


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
    """

    def __init__(self, xytheta, thetaz, currentpos, pixelsize, approachdist, depthintissue, spacingbtwn, edgecoord, ncells, speed):
        QThread.__init__(self)
        self.stopsignal = False
        self.xthetarad = xytheta # angle between vertical and man y or horz and man x
        self.thetaz = thetaz # pipette angle
        self.currentposition = currentpos # Pixel coordinates of clicked tip
        self.pixelsize = pixelsize # um per pixel
        self.approachdist = approachdist # nm of approach dist
        self.depthintissue = depthintissue # nm of depth in tissue
        self.spacingbtwn = (spacingbtwn/(self.pixelsize))
        self.edgecoords = edgecoord # list of pixel coords of annotation
        self.numbercells = ncells # desired number of injections
        self.speed = speed
        
    def __del__(self):
        self.wait()

    def run(self):
        self.implement_traj()


    def implement_traj(self):

        try:
            trajectoryarray = []
            for i in range(1,int(self.numbercells)):
                # Injection number. Hardcoded 200 injections, but just errs out with exception when the injections exceed trajectory limits (because of y stepsize)
                self.statusnumber = i
                self.motorfinished = False
                print("Injection number = ")
                print(i)

                # Stop button presed
                if self.stopsignal == True:
                    break

                # If first injection
                if i == 1:
                    # current pos = pixel coordinates of the last clicked tip
                    x0 = self.currentposition[0]
                    y0 = self.currentposition[1]
                    arrayf = self.edgecoords[int(i*self.spacingbtwn)]
                    # desired pos = pixel coordinates along annotated edge
                    xf = arrayf[0]
                    yf = arrayf[1] 

                # On subsequent injections (not first)
                if i  > 1:
                    # desired pos = pixel coordinates of injected site with spacing from just injected site
                    arrayf = self.edgecoords[int(i*self.spacingbtwn)]
                    print(int(i*self.spacingbtwn))
                    xf = arrayf[0]
                    yf = arrayf[1]
                    # current pos = pixel coordinates on the edge of the "just injected site"
                    array1 = self.edgecoords[(int((i-1)*self.spacingbtwn))]
                    x0 = array1[0]
                    y0 = array1[1]

                # Compute the desired change in pixel coordinates of the micropipette tip
                x = xf - x0
                y = yf - y0
                print('x, y = ' + str(x) +',' +str(y))
                # Calibration matrix? Idk why Gabi hardcoded the 0.033...
                # a =   [-1     -sin(thetax)]
                #       [-0     -cos(thetax)]
                #
                # where thetax = is the angle the y axis makes w/ verical and x axis makes with horizontal
                # But theta isn't signed properly or general to any orientation.
                # This matrix is only specific to the manipulator coming perpendicular from the right side of FOV
                a = np.array([[-np.cos(0.0338853299), -np.sin(self.xthetarad)], [-np.sin(0.0338853299), -np.cos(self.xthetarad)]])
                a = np.array([[-np.cos(self.xthetarad), -np.sin(self.xthetarad)], [-np.sin(self.xthetarad), -np.cos(self.xthetarad)]])
                # Desired change in pixel coordinates of the micropipette tip
                b = np.array ((x,y))
                print('a =' + str(a))
                print('b = ' + str(b))
                # Solve for the psuedo change in pixel coordiantes (as if the manipulator units were pixels) to move the micropiptte accordint to orientaiotn of maipulator axes
                manipulator = np.linalg.solve(a, b)
                print('dx,dy = ' + str(manipulator))
                # Convert the psuedo chagne in pixel coordinates to actual change in manipulator coordinates
                manipulator_motorscaled = manipulator*self.pixelsize*1000 #(in nanometers)
                print('manipulator_motorscaled =' + str(manipulator_motorscaled))
                # append change in manipualtor cooridnates to array
                trajectoryarray.append([manipulator_motorscaled])
                # Get the change in manipulator coordinates aka (k = manipulator_motorscaled). idk why gabi did this
                k = trajectoryarray[(i-1)]
                print('k = ' + str(k))
                # z corrected is actual computing necessary change in d coordiante accorording to pipette anle (thetaz)
                # cos(pipette angle) = x/d so x/cos(pipette angle) -> d
                zcorrected = (k[0][0]/(np.cos(self.thetaz)))
                print('zcorrected =' + str(zcorrected))
                zcorrected = zcorrected # why?
                # Resolve for x but negate it? because zcorrected was solved as d?
                # cos(pipette angle) = x/d so -d*cos(pipette angle -> -x
                zdrift = -zcorrected*(np.cos(self.thetaz))
                print(zdrift)

                # 4 axis trajectory (updated)
                dx = manipulator_motorscaled[0]
                dy = manipulator_motorscaled[1]
                dz_per_dd = np.sin(np.abs(self.thetaz))
                dx_per_dd = np.cos(np.abs(self.thetaz))
                self.motorcalib3 = mci(i,dx,dy,dx_per_dd,dz_per_dd,self.approachdist, self.depthintissue, self.speed)

                # 3 axis trajecotry (original)
                # self.motorcalib3 = mc(zdrift, zcorrected, k[0][1], self.approachdist, self.depthintissue, self.speed)
                
                # Run trajecotory
                self.motorcalib3.finished.connect(self.turnsignal) # when injects positoin, sends signal which will cause next injection positoin
                self.motorcalib3.start()

                # Keep waiting until injected, but then move to next position when current position injected
                while self.motorfinished == False:
                    time.sleep(0.1)
                    
            print(trajectoryarray)

        except:
            print(traceback.format_exc())
            print('except')
            print(trajectoryarray)

        #pull out last injection command...
        print('pull out start')
        dist = 400000
        pulloutlastpos = self.motorcalib3.finalpullout(dist, int(dist*self.thetaz))
        print('pulloutend')

    def turnsignal(self):
        #switches for loop to calculate and send next command to manipulator
        print('Injection complete')
        self.motorfinished = True

    def stopprocess(self):
        self.stopsignal = True
