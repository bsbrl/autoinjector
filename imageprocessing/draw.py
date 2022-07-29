import cv2
import numpy as np 
from scipy.interpolate import UnivariateSpline
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import sys

drawing = False # true if mouse is pressed
mode = True # if True, draw rectangle. Press 'm' to toggle to curve

class drawobj(object):
    """
    this class initiates a GUI for a user to select the ROI of the tip. Parameters passed into the 
    class include og which is a captured video frame at the instance the user presses "draw tip" in GUI
    """
    def __init__(self,og):
        self.error_msg = QMessageBox()
        self.error_msg.setIcon(QMessageBox.Icon.Critical)
        self.error_msg.setWindowTitle("Error")

        #og is image frame fed into function by videocontrols stream
        self.og = og
        self.drawedgecoord=[]
        self.drawedgecoord1=[]
        self.xvals = []
        self.yvals = []
        cv2.namedWindow('Draw Edge', cv2.WINDOW_AUTOSIZE)
        cv2.setMouseCallback('Draw Edge',self.interactive_drawing)
        cv2.imshow('Draw Edge',og)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def interactive_drawing(self,event,x,y,flags,param):
        global ix,iy,drawing, mode

        if event==cv2.EVENT_LBUTTONDOWN:
            drawing=True
            ix,iy=x,y

        elif event==cv2.EVENT_MOUSEMOVE:
            if drawing==True:
                if mode==True:
                    cv2.circle(self.og,(x,y),1,(0,0,255),-1)
                    cv2.imshow('Draw Edge',self.og)
                    self.xvals.append(int(x))
                    self.yvals.append(int(y))
                    self.drawedgecoord.append((x,y))
        elif event==cv2.EVENT_LBUTTONUP:
            drawing=False
            if mode==True:
                cv2.circle(self.og,(x,y),1,(0,0,255),-1)
                #self.drawedgecoord = np.asarray(self.drawedgecoord)
                self.interpolatetrajectory()
        return self.drawedgecoord1

    def interpolatetrajectory(self):
        #performs spline interpolation of coordinates along the height of the image
        yvals = np.array(self.yvals)
        xvals = np.array(self.xvals)
        order = np.argsort(self.yvals)        
        self.height = max(self.yvals)
        spl = UnivariateSpline(yvals[order],xvals[order], s = len(yvals)*3)
        ynew = np.arange(min(self.yvals),self.height,1)
        xnew = (spl(ynew))

        try:
            for i in range(0,len(xnew)-1):
                x = int(xnew[i])
                y = int(ynew[i])
                self.drawedgecoord1.append([x,y])
                if i == len(xnew)-2:
                    self.drawedgecoord1 = np.asarray(self.drawedgecoord1)
                cv2.destroyAllWindows()
        except:
            self.error_msg.setText("Cannot draw line up then down, it must go in one direction only. Close window and try again. \n Python Error = \n" + str(sys.exc_info()))
            self.error_msg.exec()
            cv2.destroyAllWindows()
