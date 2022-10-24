
import os, signal, time
from prmp_websockets import PRMP_WebSocketHandler as WSH, PRMP_WebSocketServer as WSS, PRMP_WebSocketClient as WSC


class Server(WSS):
    def on_start(self):
        print(f'\nServer started at {time.time(): .0f}')
    
    def on_new_client(self, client: WSH):
        print(f'Client {client.client_address[0]} Connected')
    
    def on_client_left(self, client: WSH):
        print(f'Client {client.client_address[0]} left')
    
    def on_accept(self, sock, addr):
        print(f'Client {addr} Accepted')


class Echo(WSH):
    def on_message(self):
        self.sendMessage(f"Echo -->{self.data}")


class Chat(WSH):

    def __init__(self, *args):
        super().__init__(*args)

    def on_message(self):
        self.send_message(f'Server AlphaHash > You said "{self.data}"')

    def on_connected(self):
        self.send_message('Server> You connected successfully')
        print('Connected')

    def on_closed(self):
        print('Disconnected')



if __name__ == "__main__":
    host = ""
    port = 8000
    websocket_handler_class = Echo
    websocket_handler_class = Chat

    websocket_server = Server((host, port), websocket_handler_class)


    def close_sig_handler(signal: signal.Signals, frame):
        websocket_server.server_close()
        # websocket_server._shutdown_gracefully()
        os.system(f'{os.sys.executable} {os.sys.argv[0]}')
        exit()

    signal.signal(signal.SIGINT, close_sig_handler)
    websocket_server.serve_forever(0)
