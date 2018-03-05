import socketio
import eventlet

sio = socketio.Server(async_mode='eventlet')
app = socketio.Middleware(sio)

pipe = None

def background_loop(drone_state):
    while True:
        sio.sleep(0.5)
        emit_drone_status(drone_state)

def emit_drone_status(state):
    required = set(['status', 'location', 'altitude', 'distance', 'speed', 'battery', 'signal'])
    state_keys = set(state.keys())
    if required == state_keys:
        sio.emit('updateDroneStatus', state.copy())

@sio.on('connect')
def connect(sid, env):
    global pipe
    pipe.send(('connected', True))

@sio.on('disconnect')
def disconnect(sid):
    global pipe
    pipe.send(('connected', False))

@sio.on('action')
def action(sid, data):
    global pipe
    pipe.send(('action', data))

@sio.on('update_all')
def update_all(sid, data):
    global pipe
    pipe.send(('update_all', data))

@sio.on('update_location')
def update_location(sid, data):
    global pipe
    pipe.send(('update_location', data))

@sio.on('set_mode')
def set_mode(sid, data):
    global pipe
    pipe.send(('set_mode', data))

@sio.on('update_manual')
def update_manual(sid, data):
    global pipe
    pipe.send(('update_manual', data))

@sio.on('update_flytopoint')
def update_flytopoint(sid, data):
    global pipe
    pipe.send(('update_flytopoint', data))

def start(drone_state, pipe_end):
    global pipe
    pipe = pipe_end
    sio.start_background_task(background_loop, drone_state)
    eventlet.wsgi.server(eventlet.listen(('', 8000)), app, log_output=False)
