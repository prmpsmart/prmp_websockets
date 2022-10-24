import imports # ignore
from prmp_websockets import PRMP_WebSocketClient



class Client(PRMP_WebSocketClient):
    
    def on_connected(self):
        ...

    def on_message(self):
        ...

    def on_ping(self):
        ...

    def on_pong(self):
        ...

    def on_closed(self):
        ...


client = Client()
client.connect(url='ws://localhost:8000')
# or
# client.connect(ip='localhost', port=8000, secure=False)
# when protocol is wss, secure is True

client.start(threaded=True)
