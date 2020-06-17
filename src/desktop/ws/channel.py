import asyncio
import exceptions

from websocket import create_connection
from queue import Queue
from threading import Thread
from types import FunctionType


class Channel:
    priority = 8  # соответствует кол-ву прерываний на async send и receive в секунду
    __halt_loop_flag = False
    __server_uri = None
    __receive_loop_coro = None
    __data_to_send = Queue()
    __receive_handlers = Queue()
    socket = None
    loop = None

    @staticmethod
    def halt_loop():
        Channel.__halt_loop_flag = True
        try:
            Channel.loop.stop()
            Channel.__receive_loop_coro.close()
        except:
            pass

    @staticmethod
    def try_connect(ip="127.0.0.1", port=8000) -> bool:
        Channel.__server_uri = f"ws://{ip}:{port}/ws/"
        Channel.__halt_loop_flag = False
        try:
            Channel.socket = create_connection(Channel.__server_uri)
        except:
            return False
        Channel.__run_channel_async()
        return True

    @staticmethod
    def disconnect():
        if Channel.socket is None:
            raise exceptions.InvalidOperationException
        Channel.halt_loop()
        Channel.socket.close()

    @staticmethod
    def ignore_next_response():
        Channel.__receive_handlers.put(None)

    @staticmethod
    def receive_now():
        return Channel.socket.recv()

    @staticmethod
    def __run_channel_async():
        def channel_loop():
            Channel.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(Channel.loop)
            Channel.__receive_loop_coro = Channel.__receive_loop()
            asyncio.ensure_future(Channel.__receive_loop_coro)
            Channel.loop.run_forever()
        Channel.__channel_thread = Thread(target=channel_loop)
        Channel.__channel_thread.start()

    @staticmethod
    async def __receive_loop():
        while True:
            while Channel.__receive_handlers.empty():
                await asyncio.sleep(1 / Channel.priority)
            if Channel.__halt_loop_flag:
                return
            handler = Channel.__receive_handlers.get()
            data = Channel.socket.recv()
            if handler is not None:
                handler(data)

    @staticmethod
    def send(data):
        if not isinstance(data, (str, bytes)):
            raise exceptions.ArgumentTypeException()
        Channel.socket.send(data)

    @staticmethod
    def receive_async(receive_handler):
        if not isinstance(receive_handler, FunctionType):
            raise exceptions.ArgumentTypeException()
        Channel.__receive_handlers.put(receive_handler)
