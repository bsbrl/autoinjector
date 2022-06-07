from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import os, sys, time
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from sensapex_utils.sensapex_utils import SensapexDevice, UMP
from .injectioncontrolmod import injection 
import numpy as np

class motorpositionThread(QThread):
    """ 
    Qthread class. This class handles getting current position of motors and sending
    out motor information to GUI, no input required.
    """
    motorpos = pyqtSignal(list)


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
            
