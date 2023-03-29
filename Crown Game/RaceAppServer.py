from multiprocessing.connection import Listener

from codrone_edu.drone import *

drone = Drone()
drone.pair()

def child(conn):
    while True:
        msg = conn.recv()

        if msg == "Takeoff":
            drone.takeoff()
        elif msg == "Land":
            drone.land()
        elif msg == "MoveForward":
            drone.move_forward(60, "cm", 0.5)

def mother(address):
    serv = Listener(address)
    while True:
        client = serv.accept()
        child(client)

mother(('', 5001))