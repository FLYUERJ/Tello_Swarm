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
        self.command_queue = queue.Queue()


        self.MAX_TIME_OUT = 15.0

    def send_command(self, command: str = None):
        """
        """
        if command:
            
            self.log.append(Stats(command, len(self.log)))

            self.socket.sendto(command.encode('utf-8'), self.tello_address_tuple)
            print(f"[INFO] Sending command: {command} to {self.ip_addr}")

            start = time.time()
            
            self.command_queue.put(command)

            while not self.log[-1].got_response(): ##this only achieves when receive messages works
                now = time.time()
                diff = now - start

                if diff > self.MAX_TIME_OUT:
                    print(f"[ERROR] Max timeout exceeded command: {command}")
                    print(f"[ERROR QUEUE] Max timeout exceeded command Queue: {self.command_queue.get()}")

            ##this queue inplementation is to try for error handlind in the future
            command_queued = self.command_queue.get()
            print(f"[INFO] Queue Item: {command_queued}")
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
    
    def getBattery(self):
        """
            GetBattery
        """

    