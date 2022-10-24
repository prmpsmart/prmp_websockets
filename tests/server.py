import imports # ignore
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
