from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import os, sys, time
from sensapex_utils.sensapex_utils import SensapexDevice, UMP
import numpy as np

class delmotor():
    """ Increase or decrease motor for given axis
    Inputs for the class are:
    axis = string, x y or z axis of desired motion ('x')
    direct = string, direction of motion ('increase' or 'decrease')
    dist = int, distance of motion
    speed = int, speed of manipulators (1000 is max)
    typeval = 'relative' or 'absolute'
    pos = position to go to (only used for absolute typeval)
    """

    def __init__(self, axis, direct, dist, speed,typeval,pos):
        self.ump = UMP.get_ump()
        self.devids = self.ump.list_devices()
        self.devs = {i:SensapexDevice(i) for i in self.devids}
        self.axis = axis
        self.direct = direct
        self.dist = dist
        self.speed = speed
        self.type = typeval
        self.posabs = pos
        #assign number to axis
        if self.axis == 'x':
            self.axisnum = 0
        elif self.axis == 'y':
            self.axisnum = 1
        elif self.axis =='z':
            self.axisnum = 2

        self.currentpos = self.devs[1].get_pos()

    def start(self):
        self.changevalue()

    def changevalue(self):
        if self.type == 'relative':
            position0 = self.devs[1].get_pos()
            position1 = position0[:]

            if self.direct == 'increase':
                position1[self.axisnum] += self.dist
            elif self.direct == 'decrease':
                position1[self.axisnum] -= self.dist
            self.devs[1].goto_pos(position1,self.speed)

        if self.type == 'absolute':
            position1 = self.dist
            self.devs[1].goto_pos(position1,self.speed)


        #functions just to get the position of the manipulator, used in resolution test functions
        if self.type == 'getposition_m0':
            x = 'self.m0' in vars()
            if x == False:
                self.m0 = self.devs[1].get_pos()
                print('wtf')
            else:
                print('no update')

        if self.type == 'getposition_m1':
            self.m1 = self.devs[1].get_pos()

        if self.type == 'getposition_m2':
            self.m2 = self.devs[1].get_pos()
