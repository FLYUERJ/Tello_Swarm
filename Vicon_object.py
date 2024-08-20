import queue
import socket
import threading
import time
from stats import Stats
import pyvicon
import time
from enum import Enum
from pyvicon import StreamMode, Direction
from paulo_tello import Tello_Paulo


class DroneVicon:

    def __init__(self,DroneConn: Tello_Paulo) -> None:

        self.DroneConnection : Tello_Paulo = DroneConn
        self.viconConnection = pyvicon.PyVicon()
        self.Xposition = None
        self.Yposition = None
        self.Zposition = None
    
    def connectVicon(self,ip:str)
        self.vicon.connect(ip)
        print(self.vicon.is_connected())

        self.vicon.enable_device_data()
        self.vicon.enable_segment_data()
        self.vicon.enable_marker_data()
        self.vicon.enable_unlabeled_marker_data()

    
