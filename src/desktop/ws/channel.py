import exceptions
import websockets
import asyncio

from queue import Queue
from threading import Thread
from types import FunctionType


# TODO: задокументировать


class Channel:
    priority = 2  # соответствует кол-ву прерываний на async send и receive в секунду
    __connecting_failed = False
    __server_uri = None
    socket = None

    @staticmethod
    def try_connect(ip="127.0.0.1", port=8000) -> bool:
        Channel.__server_uri = f"ws://{ip}:{port}/ws/"
        Channel.__connecting_failed = False
        Channel.__run_channel_async()
        while (Channel.socket is None) and not Channel.__connecting_failed:
            pass
        return not Channel.__connecting_failed

    @staticmethod
    async def __connect(uri):
        try:
            Channel.socket = await websockets.connect(uri)
        except:
            Channel.__connecting_failed = True

    @staticmethod
    def receive_now() -> str:
        return Channel.socket.recv()

    # vvv async tools vvv

    @staticmethod
    def __run_channel_async():
        def channel_loop():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            asyncio.ensure_future(Channel.__connect(Channel.__server_uri))
            asyncio.ensure_future(Channel.__send_loop())
            asyncio.ensure_future(Channel.__receive_loop())
            loop.run_forever()
        Channel.__channel_thread = Thread(target=channel_loop)
        Channel.__channel_thread.start()

    @staticmethod
    def close_channel_thread():
        Channel.__channel_thread.join()
        del Channel.__channel_thread

    __data_to_send = Queue()
    __receive_handlers = Queue()

    @staticmethod
    async def __send_loop():
        while True:
            while Channel.__data_to_send.empty():
                await asyncio.sleep(1 / Channel.priority)
            data = Channel.__data_to_send.get()
            await Channel.socket.send(data)

    @staticmethod
    async def __receive_loop():
        while True:
            while Channel.__receive_handlers.empty():
                await asyncio.sleep(1 / Channel.priority)
            handler = Channel.__receive_handlers.get()
            data = await Channel.socket.recv()
            handler(data)

    @staticmethod
    def send(data: str):
        if not isinstance(data, str):
            raise exceptions.ArgumentTypeException()
        Channel.__data_to_send.put(data)

    @staticmethod
    def receive_async(receive_handler):
        if not isinstance(receive_handler, FunctionType):
            raise exceptions.ArgumentTypeException()
        Channel.__receive_handlers.put(receive_handler)
