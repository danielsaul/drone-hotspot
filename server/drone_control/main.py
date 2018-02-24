from multiprocessing import Process, Pipe, Manager

from control import Control
import socket

def drone_control(drone_state, pipe):
    c = Control(drone_state, pipe)
    c.start()

def main():

    print "Drone Hotspot Control"

    # Setup multiprocessing
    manager = Manager()
    drone_state = manager.dict()
    socket_pipe, control_pipe = Pipe()

    # Start control process
    print "Starting control process..."
    controlproc = Process(target=drone_control, args=(drone_state, control_pipe))
    controlproc.start()

    # Start comms with phone app
    print "Starting socket connection..."
    socket.start(drone_state, socket_pipe)


