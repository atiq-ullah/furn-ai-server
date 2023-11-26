import socketio

sio = socketio.AsyncServer(async_mode='asgi')
app = socketio.ASGIApp(sio)

@sio.event
async def connect(sid, environ):
    print('Socket.IO client connected:', sid)

@sio.event
async def disconnect(sid):
    print('Socket.IO client disconnected:', sid)

# Add more event handlers as needed
