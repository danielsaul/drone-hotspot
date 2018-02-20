import socketio
import eventlet

sio = socketio.Server(async_mode='eventlet')
app = socketio.Middleware(sio)

def background_loop(drone_state):
    while True:
        sio.sleep(0.5)
        emit_drone_status(drone_state)

def emit_drone_status(state):
    required = set(['status', 'location', 'altitude', 'distance', 'speed', 'battery', 'signal'])
    state_keys = set(state.keys())
    if required != state_keys:
        raise ValueError("State does not include all the required keys")

    sio.emit('updateDroneStatus', state)

def start(drone_state):
    sio.start_background_task(background_loop, drone_state)
    eventlet.wsgi.server(eventlet.listen(('', 8000)), app)
