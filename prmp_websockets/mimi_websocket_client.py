
import signal
import time
from prmp_websockets import PRMP_WebSocketClient as WSC



class Chat(WSC):

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
    host, port = 'localhost', 8000
    client = Chat()
    client.connect(address=host, port=port)
    
    def close_sig_handler(signal: signal.Signals, frame):
        # os.system(f'{os.sys.executable} {os.sys.argv[0]}')
        client.send_close(reason='Test')
        client.shutdown()


    signal.signal(signal.SIGINT, close_sig_handler)

    client.start()

    # while client.connected:
    #     print(time.sleep(3))
    #     print(time.time())
    # client.send(b'Test')
    # print(client.recv())
