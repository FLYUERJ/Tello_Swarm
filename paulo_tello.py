import queue
import socket
import threading
import time
from stats import Stats

#wont implement video yet

class Tello_Paulo:
    def __init__(self, wifi_interface : str = None) -> None:
        self.ip_addr = "192.168.10.1"
        self.port = 8889
        ## AF address family internet, DGRAM-> Datagram socket (UDP)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if wifi_interface:
            self.socket.setsockopt(socket.SOL_SOCKET, 25, wifi_interface.encode())
        
        self.tello_address_tuple = (self.ip_addr, self.port)

        ## intializing the thread to receive command from tello

        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.daemon = True
        self.receive_thread.start()

        self.log = []
        self.response_map = {}


        self.MAX_TIME_OUT = 15.0

    def send_command(self, command: str = None):
        """
        """
        if command:
            
            self.log.append(Stats(command, len(self.log)))

            self.socket.sendto(command.encode('utf-8'), self.tello_address_tuple)
            print(f"[INFO] Sending command: {command} to {self.ip_addr}")

            start = time.time()
            
            self.response_map["command"] = None

            while not self.log[-1].got_response(): ##this only achieves when receive messages works
                now = time.time()
                diff = now - start

                if diff > self.MAX_TIME_OUT:
                    print(f"[ERROR] Max timeout exceeded command: {command}")
                    print(f"[ERROR QUEUE] Max timeout exceeded command Queue: {self.command_queue.get()}")

            ##this queue inplementation is to try for error handlind in the future
            self.response_map[command] = self.log[-1].get_response()
            print(f"[INFO] Done!!! sent command: {command} to {self.ip_addr}")
            return
        
        print("Command not Send")

    def receive_messages(self):
        """
            Listen responses in another thread from tello
        """

        while True:
            try:
                self.response , ip = self.socket.recvfrom(1024)
                print(f"from {ip}: {self.response} ")
                
                self.log[-1].add_response(self.response.decode("utf-8"))

            except socket.error:
                print(f"[ERROR] Caught exception socket.error {socket.error}")
            except Exception as ex:
                print(f"[ERROR] Extra errors: {ex}")

    def connect(self):
        """
            Connect using Command
        """
        return self.send_command("command")
    ##GET MODEL IS IN THAT WAY THAT YOU NEED TO GET STATUS FROM DRONE
    def getBattery(self) -> int:
        """
            GetBattery
        """
        self.send_command("battery?")

        if(self.response_map["battery?"] is not None):
            return int(self.response_map["battery?"])
        else:
            print("[ERROR] Cannot get Battery")
            return -1
        
    def takeoff(self):
        """
            Takeoff drone
        """
        return self.send_command("takeoff")
    
    def land(self):

        return self.send_command("land")
    
    def moveUp(self, distance : int ):

        if(distance >= 20 and distance <= 500):
            return self.send_command(f"up {distance}")
        else:
            print("[ERROR] distance need to be between 20-500")
    
    def movedown(self, distance : int ):

        if(distance >= 20 and distance <= 500):
            return self.send_command(f"down {distance}")
        else:
            print("[ERROR] distance need to be between 20-500")
    
    def moveleft(self, distance : int ):

        if(distance >= 20 and distance <= 500):
            return self.send_command(f"left {distance}")
        else:
            print("[ERROR] distance need to be between 20-500")
    
    def moveright(self, distance : int ):

        if(distance >= 20 and distance <= 500):
            return self.send_command(f"right {distance}")
        else:
            print("[ERROR] distance need to be between 20-500")
    
    def moveforward(self, distance : int ):

        if(distance >= 20 and distance <= 500):
            return self.send_command(f"forward {distance}")
        else:
            print("[ERROR] distance need to be between 20-500")
    
    def moveback(self, distance : int ):

        if(distance >= 20 and distance <= 500):
            return self.send_command(f"back {distance}")
        else:
            print("[ERROR] distance need to be between 20-500")

    def rotateClockWise(self, distance : int):

        if(distance >= 1 and distance <= 3600):
            return self.send_command(f"cw {distance}")
        else:
            print("[ERROR] distance need to be between 1-3600")

    def rotateCounterClockWise(self, distance : int):

        if(distance >= 1 and distance <= 3600):
            return self.send_command(f"ccw {distance}")
        else:
            print("[ERROR] distance need to be between 1-3600")
    
    def goXYZdirection(self, x : int,y : int, z : int, speed: int):
        
        if(speed >= 10 and speed <= 100):
            return self.send_command(f"go {x} {y} {z} {speed}")
    