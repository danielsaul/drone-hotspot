import asyncio

from aiohttp import web

import socketio

sio = socketio.AsyncServer(async_mode='aiohttp')
app = web.Application()
sio.attach(app)


async def background_task():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        await sio.sleep(0.1)
        count += 1
        await sio.emit('test', str(count))

@sio.on('disconnect', namespace='/test')
def test_disconnect(sid):
    print('Client disconnected')



if __name__ == '__main__':
    sio.start_background_task(background_task)
    web.run_app(app, host='127.0.0.1', port=8080)
