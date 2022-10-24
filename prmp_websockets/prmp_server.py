# from prmp_websockets import *
import websockets


# class AmeboClientHandler(PRMP_WebSocketHandler):
#     def handle_connected(self):
#         return super().handle_connected()

#     def handle_closed(self):
#         return super().handle_closed()

#     def handle_message(self):
#         return super().handle_message()

#     def handle_pong(self):
#         return super().handle_pong()

#     def handle_ping(self):
#         return super().handle_ping()


# class AmeboServer(PRMP_WebSocketServer):
    # def __init__(self, server_address: tuple[str, int], **kwargs) -> None:
    #     super().__init__(server_address, AmeboClientHandler, **kwargs)

    # def new_client(self, client: PRMP_WebSocketHandler):
    #     return super().new_client(client)

    # def client_left(self, client: PRMP_WebSocketHandler, server: PRMP_WebSocketServer):
    #     return super().client_left(client, server)

app = websockets.WebSocketApp()
