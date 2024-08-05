from paulo_tello import Tello_Paulo
import time
import threading

def executeAsync(drone : Tello_Paulo):

    drone.connect()

    time.sleep(0.01)
    drone.send_command("battery?")

    time.sleep(0.1)
    drone.send_command("takeoff")

    time.sleep(5)

    drone.send_command("land")

drone1 = Tello_Paulo("wlx50016b32a1cd")
drone2 = Tello_Paulo("wlxf085c1c9e7eb")

task_thread_drone1 = threading.Thread(target=executeAsync, args=(drone1,))
task_thread_drone2 = threading.Thread(target=executeAsync, args=(drone2,))

task_thread_drone1.start()
task_thread_drone2.start()

print("ASSSYYYNC")
while True:
    pass