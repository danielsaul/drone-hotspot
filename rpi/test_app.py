import asyncio

from aiohttp import web

import socketio

sio = socketio.AsyncServer(async_mode='aiohttp')
app = web.Application()
sio.attach(app)


status = "waiting"

async def background_task():
    data = {
        'status': "waiting",
        'location': {'latitude': 51.3496, 'longitude': -0.22883},
        'altitude': 0,
        'distance': 0,
        'speed': 0.0,
        'battery': 95,
        'signal': 4
    }

    while True:
        await sio.sleep(1)
        data['battery'] -= 0.5
        global status
        if status == "flying":
            data['location']['latitude'] += 0.00001
            data['altitude'] += 0.5
            data['speed'] = 2
            data['status'] = "flying"
        elif status == "landing":
            data['altitude'] -= 2
            if data['altitude'] <= 0:
                data['altitude'] = 0
                data['status'] = "waiting"
                data['speed'] = 0
                status = "waiting"

        await sio.emit('updateDroneStatus', data)


@sio.on('update_all')
def update_all(sid, data):
    #print(data)
    pass

@sio.on('update_location')
def manual(sid, data):
    print(data)

@sio.on('action')
def action(sid, data):
    global status
    if data == 'takeoff':
        print("Taking off.")
        status = "flying"
    elif data == 'land':
        print("Landing.")
        status = "landing"
    elif data == 'return':
        print("Returning.")
        status = "returning"
    elif data == 'abort':
        print("ABORT")
        status = "abort"




if __name__ == '__main__':
    sio.start_background_task(background_task)
    web.run_app(app, host='0.0.0.0', port=8080)
