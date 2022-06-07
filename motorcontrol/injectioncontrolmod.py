from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import serial
import time
import numpy as np

class injection(QThread):
    """ 
    This class handles injection protocol commands to the arduino. 
    Inputs are all numerical except the serial object arduino and pressureortrigger:
    ard = arduino serial object
    backpressure = backpressure voltage to apply to prevent clogging of tip (0-255)
    ninjections = number of injections/cell
    injectionvoltage = pressure voltage to control injection pressure (0 - 255)
    pulseduration = pulse duration of triggering pressure(ms)
    bporpressureortrigger = character value 'bp', 'p', or 't' will either set compensation pressure, injection pressure, or trigger injection,respectively
    """

    #injectionstatus = pyqtSignal(str)

    def __init__(self,ard,backpressure,ninjections,injectionvoltage,pulseduration,bporpressureortrigger):
        QThread.__init__(self)
        self.compensatepressure = backpressure
        self.arduino = ard
        self.ninject = ninjections
        self.injectvoltage = injectionvoltage
        self.pulse = pulseduration
        self.bporpressureortrigger = bporpressureortrigger
        self.pressurefinished = False
        self.triggercomplete = False

    def __del__(self):
        self.wait()

    def run(self):
        """
        This is what is called when the class is going and controls the execution of thread
        """
        if self.bporpressureortrigger == 'bp':
            print('bp selected')
            self.bppressureString()
            self.sendcommand(self.send)
            self.pressurefinished = True

        if self.bporpressureortrigger == 't':
            print('t selected')
            self.triggerString()
            self.sendcommand(self.send)
            self.triggercomplete = True
            self.pressurefinished = True
            print(self.triggercomplete)

    def bppressureString(self):
        self.send1 = "b" +"c" + str(self.compensatepressure) +"C"
        self.send = self.send1 + "pressure"+"!"+str(self.injectvoltage)+"!"
        print(self.send)

    def triggerString(self):
        if self.ninject < 10:
            self.ninjections_string = "0" + str(self.ninject)
        elif self.ninject >= 10:
            self.ninjections_string = str(self.ninject)

        if self.pulse < 10:
            self.pulse_string = "0" + str(self.pulse)
        elif self.pulse >= 10:
            self.pulse_string = str(self.pulse)

        self.send = "trigger" + "n" + self.ninjections_string + "N" + "w" + self.pulse_string + "W"

    def sendcommand(self,send):
        sendcommand = self.send
        self.sendfinal = ('string sent from python ' + self.send)
        self.arduino.flush()
        self.arduino.write(sendcommand)
        self.listen()

    def listen(self):
        time.sleep(0.1)
        self.response = self.arduino.read(self.arduino.inWaiting())
        print(self.response)
        self.recieve = ('string python recieved from arduino ' + str(self.response))
