# prmp_websockets

A websockets library that is very easy to handle, with little to no hacks.

## Tests

- [tests/server.py](tests/server.py)
``` python

from prmp_websockets import PRMP_WebSocketServer, PRMP_WebSocketHandler


class ClientHandler(PRMP_WebSocketHandler):
    
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

class Server(PRMP_WebSocketServer):
    def __init__(self, **kargs) -> None:
        super().__init__(RequestHandlerClass=ClientHandler, **kargs)
    
    def on_accept(self, sock, addr):
        ...

    def on_start(self):
        ...

    def on_new_client(self, client: ClientHandler):
        ...

    def on_client_left(
        self,
        client: ClientHandler,
    ):
        ...

ip, port = 'localhost', 8000
server = Server(server_address=(ip, port))
server.serve_forever(threaded_serving=True)

```

- [tests/client.py](tests/client.py)
``` python
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
```
