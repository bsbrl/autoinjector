# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import os, sys, time
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from sensapex_utils.sensapex_utils import SensapexDevice, UMP
import numpy as np

class GetPos(QThread):

    def __init__(self, currentpos, futurepos, motorposstart,speed, xmotortheta, thetaz, pixelsize):
        # currentpos = x,y camera coordinate of current position
        # futurepos = x,y camera coordinate of future position (point on restest grid)
        # motorposstart = the manipulator current position
        # speed = speed of manipulator in microns/s
        # x motortheta = 

        QThread.__init__(self)

        #assign axes -> this is used when switching between 3-axis and 4-axis sensapex
        self.yaxis = 1
        self.zaxis = 2

        if len(motorposstart) == 3:
            self.xaxis = 0
        elif len(motorposstart) == 4:
            self.xaxis = 3

        print('currentpos' + str(currentpos))
        print('futurepos' + str(futurepos))

        self.make_commands(currentpos,futurepos,motorposstart,xmotortheta,thetaz,pixelsize)


    def make_commands(self,currentpos,futurepos,motorposstart,xtheta,thetaz,pixelsize):

        print('start pos = ' + str(motorposstart))

        # calculate distance from desired point to current point
        xdist = futurepos[self.xaxis] - currentpos[self.xaxis]
        ydist = futurepos[1] - currentpos[1]
        print('x, y = ' + str(xdist) +',' +str(ydist))	

        #convert from pixel distance to manipulator distance for future pos
        a = np.array([[-np.cos(xtheta), -np.sin(xtheta)], [-np.sin(xtheta), -np.cos(xtheta)]])
        b = np.array ((xdist,ydist))
        print('xtheta = ' +str(xtheta))
        print('pixelsize =' + str(pixelsize))
        print('a =' + str(a))
        print('b = ' + str(b))
        disttopoint = np.linalg.solve(a, b)
        print('dx,dy = ' + str(disttopoint))
        disttopoint_scaled = disttopoint*pixelsize*1000 
        print('manipulator_motorscaled =' + str(disttopoint_scaled))

        futuremotor = motorposstart
        zcorrected = (disttopoint_scaled[0]/(np.cos(thetaz)))  
        print('zcorrected =' + str(zcorrected)) 
        
        """
        if b[0] <= 0:
            offset = 2500
        else:
            offset = 2150
        """
        offset = 0

        zcorrected = zcorrected-offset
        zdrift = -zcorrected*(np.cos(thetaz))

        print('zcorrected =' + str(zcorrected)) 
        print('zdrift =' + str(zdrift)) 

        futuremotor[self.zaxis] = futuremotor[self.zaxis] + zdrift
        futuremotor[self.xaxis] = futuremotor[self.xaxis] + zcorrected
        
        print('zcorrected, zdrift =' + str(futuremotor))

        futuremotor[self.yaxis] = futuremotor[self.yaxis] + disttopoint_scaled[1]

        print('future final =' + str(futuremotor))
        self.futuremotor = futuremotor

#if __name__ == '__main__':
#	x = GoToPos((960, 730),(320, 730),[12303720.596242707, 14171260.937382057, 3713230, 10011040],1000,0.78,0.78,1.2)