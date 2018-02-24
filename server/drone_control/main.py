from multiprocessing import Process, Pipe, Manager

from control import Control
import socket

def drone_control(drone_state, pipe):
    c = Control(drone_state, pipe)
    c.start()

def main():

    # Setup multiprocessing
    manager = Manager()
    drone_state = manager.dict()
    socket_pipe, control_pipe = Pipe()

    # Start control process
    controlproc = Process(target=drone_control, args=(drone_state, control_pipe))
    controlproc.start()

    # Start comms with phone app
    socket.start(drone_state, socket_pipe)


