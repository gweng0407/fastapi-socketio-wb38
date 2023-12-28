# -*- coding: cp949 -*-
from fastapi import FastAPI ,Cookie, File, UploadFile, Request, WebSocket
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles #���� ����?
import socketio
import socket 
import uvicorn
from collections import  defaultdict
import os
import threading 
app : FastAPI = FastAPI()
app.mount('/static', StaticFiles(directory='kamos_static'), name='kamos_static')#���� ����?

# �񵿱� ���� ����
sio : socketio.AsyncServer = socketio.AsyncServer(async_mode='asgi',  
                          credits=True,
                           cors_allowed_origins = [
                           'http://localhost:5000',
                           'https://admin.socket.io',
                           'http://127.0.0.1:5000'  # �߰�: Socket.IO ������ �ּҸ� ���]
                           ])  

#������ ��� ���� ����
# sio.instrument(auth=False) # ���� ���� �����ϱ�
sio.instrument({'username':'WB38' , 'password':os.environ['WB38']})

#socketIO�� FastAPI�� ��ġ��
combined_asgi_app = socketio.ASGIApp(sio, app)

#�Ŵ��� ��������
manager = sio.manager



""" [��û�� ����]
[Request]
sio.emit('roomremove',roomname)

[Response]
@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")

@sio.on('disconnect')
def disconnected(sid,*args, **kwargs) :
"""

@app.get('/')
def index():
    # return FileResponse('kamos.html', media_type="text/html")
    return FileResponse("kamos.html")


@app.get("/navigate")
def navigate_to_another_page():
    return FileResponse("Entered.html")

@app.get("/p2pPage")
def navigate_to_another_page():
    return FileResponse("P2Ppage.html")



@sio.event
async def Message(sid, data):
    print(f"Recieved: {data}")
    await sio.emit('Message',f"Echo : {data}")

@sio.event
async def RequestConnectP2P(sid, data):
    print(f"RequestConnectP2P: {sid}")
    await sio.emit('Connect')



@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        data = await websocket.receive_text()
        await sio.emit("message", data)


@sio.on("start_p2p")
async def handle_start_p2p(sid, offer):
    print(offer)
    await sio.emit("sdp", {"sdp": offer}, room=sid)

@sio.on("send_data_channel")
async def handle_send_data_channel(sid, data):
    await sio.emit("send_data_channel", {"dataChannel": data["dataChannel"]}, room=sid)

@sio.on("sdp")
async def handle_sdp(sid, data):
    await sio.emit("sdp", {"sdp": data["sdp"]}, room=sid)

@sio.on("ice_candidate")
async def handle_ice_candidate(sid, data):
    await sio.emit("ice_candidate", {"candidate": data["candidate"]}, room=sid)





if __name__ == '__main__':
    uvicorn.run(combined_asgi_app, host='127.0.0.1', port=5000)