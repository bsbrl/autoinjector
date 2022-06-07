from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import os, sys, time
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from sensapex_utils.sensapex_utils import SensapexDevice, UMP
from .injectioncontrolmod import injection 
import numpy as np

class motorcontroller(QThread):
    """ QThread class to control 3-axis sensapex manipulators. 
    Inpts for movement are:
    zdrift 
    stepsizex (distance into tissue)
    stepsizey (distance between injections)
    approachdist = the distance from the edge of the tissue that the pipette pulls out after each injection  (taken from user input in GUI)
    injectiondepth = the depth of injection (taken from user input in GUI)
    ncells (number of steps in y to make)
    """

    signal = pyqtSignal(str)

    def __init__(self, zdrift, stepsizex, stepsizey, approachdist, injectiondepth, speed):
        QThread.__init__(self)
        self.ump = UMP.get_ump()
        self.devids = self.ump.list_devices()
        self.devs = {i:SensapexDevice(i)
         for i in self.devids}
        self.zdrift = zdrift
        self.stepsizex = stepsizex
        self.stepsizey = stepsizey
        self.approachdist = approachdist
        self.injectiondepth = injectiondepth
        self.speed = speed

    def __del__(self):
        self.wait()

    def run(self):
        self.run_trajectory()

    def run_trajectory(self):
        position0 = self.devs[1].get_pos() #current position
        print("position0 = " +str(position0))
        
        #sometimes there is an error with the sensapex manipulator and it says its position is zero, this ruins the trajectory
        if position0[0] < 100:
            print('sensapex error, wait')
            time.sleep(0.3)
            position0 = self.devs[1].get_pos() #the delay should fix it        

        # if using a 3-axis manipulator, the xaxis is 0. Else, it's 3
        if len(position0) == 3:
            xaxis = 0
        elif len(position0) == 4:
            xaxis = 3

        #go to edge of tissue 
        position1 = position0[:]
        position2 = position1[:]
        position2[xaxis] += (self.stepsizex)
        self.devs[1].goto_pos(position2, self.speed)
        print("edge of tissue" + str(position2))
        time.sleep(0.25)

        #go into tissue and inject
        pos2 = position2
        position3 = position2[:]
        position3[xaxis] += self.injectiondepth
        self.devs[1].goto_pos(position3, self.speed)
        print("injection depth =" +str(self.injectiondepth))
        print("injection site" + str(position3))
        time.sleep(0.25)

        #pull out of tissue
        posfinalout = position3[:]
        posfinalout[xaxis]-= (self.injectiondepth+self.approachdist)
        self.devs[1].goto_pos(posfinalout, self.speed)
        print("pull out tissue position = " + str(posfinalout))
        time.sleep(0.25)
        
        #step along tissue in y direction
        positiony = posfinalout[:]
        positiony[1] += self.stepsizey
        self.devs[1].goto_pos(positiony, self.speed)
        print("move in y pos = " + str(positiony))
        time.sleep(0.25)

        #correct for Zdrift if applicable
        positionzdrift = positiony[:]
        positionzdrift[2] += self.zdrift
        self.devs[1].goto_pos(positionzdrift, self.speed)
        print("z drift position = " + str(positionzdrift))
        time.sleep(0.25)

        #go to edge of tissue
        positionedge = positionzdrift[:]
        positionedge[xaxis] += self.approachdist
        self.devs[1].goto_pos(positionedge, self.speed)
        time.sleep(0.25)
        print("final position = " + str(positionedge))
                

    def finalpullout(self, dist, zdist):
        current_pos = self.devs[1].get_pos()

        #in some cases, sensapex does not report a correct xyz pos, thus we wait
        while len(current_pos) < 3:
            current_pos = self.devs[1].get_pos()
            time.sleep(0.01)      
            print("current pos =" + str(current_pos))

        #gets xaxis if 3 vs 4 axis manipulator
        if len(current_pos) == 3:
            xaxis = 0
        elif len(current_pos) == 4:
            xaxis = 3

        #in some cases, sensapex says xaxis = 2, but this is just a bug so we wait
        while current_pos[xaxis] == 2:
            current_pos = self.devs[1].get_pos()
            time.sleep(0.01)
            print("error, new current pos =" + str(current_pos))

        end_pos = current_pos[:]
        end_pos[xaxis] -= dist
        end_pos[2] += zdist
        print("end pos =" + str(end_pos))
        self.devs[1].goto_pos(end_pos, 1000)




#---------------------Thread Class for motor position----------------------------
class motorpositionThread(QThread):
    """ 
    Qthread class. This class handles getting current position of motors and sending
    out motor information to GUI, no input required.
    """
    motorpos = pyqtSignal(list)
    motorposnum = []

    def __init__(self):
        QThread.__init__(self)
        ump = UMP.get_ump()
        self.devids = ump.list_devices()
        self.devs = {i:SensapexDevice(i) for i in self.devids}

    def __del__(self):
        self.wait()

    def _get_position(self):
        """
        asks motors for position, return [x,y,z] in uM 
        """ 
        self.print_pos()
        self.current_motor = self.devs[1].get_pos()
        print(self.current_motor)
        try:
            self.motorposition = self.pos_numerical
            return self.motorposition
        except:
            print('Manipulator error')

    def print_pos(self,timeout=None):
        line = ""
        for i in self.devids:
            self.dev = self.devs[i]
            try:
                pos = str(self.dev.get_pos(timeout=timeout))
                pos_numerical = self.dev.get_pos(timeout=timeout)
                self.pos_numerical = pos_numerical
            except Exception as err:
                pos = str(err.args[0])
                self.pos_numerical = [0,0,0]
            self.pos = pos + " " * (30 - len(pos))

    def run(self):
        """ 
        what actually calls _get_position and emits the signal
        """

        while True:
            motorposition = self._get_position()
            try:
                self.motorpos.emit(motorposition)
            except:
                print('manipulator error')
            self.sleep(1)
            
