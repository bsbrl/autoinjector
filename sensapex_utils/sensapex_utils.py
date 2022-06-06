'''
Extends sensapex UMP and SensapexDevice classes to mimic behaviour or earlier
SDK. Development was orginally done with SDK 0.834 where positions were in um.
New version of SDK uses nm, so these classes are designed to mimic old
behaviour (without needing to change robotic injector code) Also, queries the
sensapex device angle.
'''
import sensapex
from ctypes import c_int, c_float, byref
import time

class UMP(sensapex.UMP):
    '''
    Extends of sensapex.UMP class

    Modifies UMP class to work with nm (instead of um) its get_pos and goto_pos
    fcns. Also extends UMP class to include option to query sensapex's d-axis
    angle.
    ''' 
    def __init__(self, address, group, start_poller=True):
        super().__init__(address, group, start_poller)

    def get_pos(self, dev:int, timeout:int=0) -> list:
        '''
        Return the absolute position of the specified device (in nm).
        
        If *timeout* == 0, then the position is returned directly from cache
        and not queried from the device.

        Arguments:
            dev (int): Sensapex device ID
            timeout (int): Time limit for query from cache (ms?)

        Returns:
            List of axis positions in nm [x_nm, y_nm, z_nm, d_nm] 
        '''
        um_pos = super().get_pos(dev=dev,timeout=timeout)
        nm_pos = [int(axis_pos*1000) for axis_pos in um_pos]
        return nm_pos

    def goto_pos(self, dev:int, dest:list, speed:float, simultaneous:bool=True, linear:bool=False, max_acceleration:int=0) -> int:
        '''
        Request the specified device to move to an absolute position (in nm).

        Arguments:
            dev (int): Sensapex device ID
            dest (list): [x,y,z,d] positions to move to in nm. Values may be
                NaN or omitted to leave the axis unaffected.
            speed (float): Manipulator speed in um/s
            simultaneous (bool): When true, all axes move simulatneously
            linear (bool): When true, axis speeds scaled to produce psuedo-
                linear movement. Requires simultaneous.
            max_acceleration (int): Maximum acceleration in um/s^2
        
        Returns:
            move_id (int): Unique ID that can be used to retrieve the status of
                this move at a later time.
        '''
        um_pos = [axis_pos/1000 for axis_pos in dest]
        return super().goto_pos(dev,um_pos, speed, simultaneous, linear, max_acceleration)

    def get_axis_angle(self, dev:int) -> float:
        '''
        Returns d-axis angle in degrees of selected uMp device
        
        Arguments:
            dev (int): Sensapex device ID
            
        Returns:
            d-axis angle in degrees of sensapex device with device number
        '''
        # ump_get_axis_angle returns angle in degrees*10
        return ump.call("ump_get_axis_angle",c_int(self.dev_id),
                        byref(c_float()))/10

class SensapexDevice(sensapex.SensapexDevice):
    '''
    Extends of sensapex.SensapexDevice

    Modifies SensapexDevice class to work with nm (instead of um) its get_pos
    and goto_pos fcns. Also extends UMP class to include option to query
    sensapex's d-axis angle.
    ''' 
    def __init__(self, dev_id: int, callback=None, n_axes=None, max_acceleration=0):
        super().__init__(dev_id,callback,n_axes,max_acceleration)

    def get_pos(self, timeout:int=None) -> list:
        '''
        Return the absolute position of the specified device (in nm).
        
        If *timeout* == 0, then the position is returned directly from cache
        and not queried from the device.

        Arguments:
            timeout (int): Time limit for query from cache (ms?)

        Returns:
            List of axis positions in nm [x_nm, y_nm, z_nm, d_nm] 
        '''
        um_pos = super().get_pos(timeout=timeout)
        nm_pos = [int(axis_pos*1000) for axis_pos in um_pos]
        return nm_pos

    def goto_pos(self, pos:int, speed:float, simultaneous:bool=True, linear:bool=False, max_acceleration:int=0) -> int:
        '''
        Request the specified device to move to an absolute position (in nm).

        Arguments:
            dest (list): [x,y,z,d] positions to move to in nm. Values may be
                NaN or omitted to leave the axis unaffected.
            speed (float): Manipulator speed in um/s
            simultaneous (bool): When true, all axes move simulatneously
            linear (bool): When true, axis speeds scaled to produce psuedo-
                linear movement. Requires simultaneous.
            max_acceleration (int): Maximum acceleration in um/s^2
        
        Returns:
            move_id (int): Unique ID that can be used to retrieve the status of
                this move at a later time.
        '''
        um_pos = [axis_pos/1000 for axis_pos in pos]
        return super().goto_pos(um_pos, speed, simultaneous, linear, max_acceleration)

    def get_axis_angle(self) -> float:
        ''' Returns d-axis angle in degrees of selected uMp device '''
        # ump_get_axis_angle returns angle in degrees*10
        return ump.call("ump_get_axis_angle",c_int(self.dev_id),
                        byref(c_float()))/10
    