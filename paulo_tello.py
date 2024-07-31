import socket
import threading
import time
from stats import Stats

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

        self.MAX_TIME_OUT = 15.0

    def send_command(self, command: str = None):
        """
        """
        if command:
            
            self.log.append(Stats(command, len(self.log)))

            self.socket.sendto(command.encode('utf-8'), self.tello_address_tuple)
            print(f"Sending command: {command} to {self.ip_addr}")

            start = time.time()

            while not self.log[-1].got_response(): ##this only achieves when receive messages works
                now = time.time()
                diff = now - start

                if diff > self.MAX_TIME_OUT:
                    print(f"Max timeout exceeded command: {command}")

            print(f"Done!!! sent command: {command} to %{self.ip_addr}")

    def receive_messages(self):
        """
            Listen responses in another thread from tello
        """

        while True:
            try:
                self.response , ip = self.socket.recvfrom(1024)
                print(f"from {ip}: {self.response} ")

                self.log[-1].add_response(self.response)
                
            except socket.error:
                print(f"Caught exception socket.error {socket.error}")