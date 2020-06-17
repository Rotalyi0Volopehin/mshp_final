import exceptions

from websocket import create_connection
from types import FunctionType


class Channel:
    __server_uri = None
    socket = None

    @staticmethod
    def try_connect(ip="127.0.0.1", port=8000) -> bool:
        Channel.__server_uri = f"ws://{ip}:{port}/ws/"
        try:
            Channel.socket = create_connection(Channel.__server_uri)
            return True
        except:
            return False

    @staticmethod
    def disconnect():
        if Channel.socket is None:
            raise exceptions.InvalidOperationException
        Channel.socket.close()
        Channel.socket = None

    @staticmethod
    def receive():
        return Channel.socket.recv()

    @staticmethod
    def send(data):
        if not isinstance(data, (str, bytes)):
            raise exceptions.ArgumentTypeException()
        Channel.socket.send(data)

    @staticmethod
    def receive_async(receive_handler):
        if not isinstance(receive_handler, FunctionType):
            raise exceptions.ArgumentTypeException()
        data = Channel.socket.recv()
        receive_handler(data)
