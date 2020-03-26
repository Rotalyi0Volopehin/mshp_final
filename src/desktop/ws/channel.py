import exceptions
import websockets
import time
import asyncio

from queue import Queue
from threading import Thread


# TODO: задокументировать


class Channel:
    priority = 2  # соответствует кол-ву прерываний на async send и receive в секунду

    @staticmethod
    def try_connect(ip="127.0.0.1", port=8000) -> bool:
        uri = f"ws://{ip}:{port}/ws/"
        try:
            asyncio.get_event_loop().run_until_complete(Channel.__connect(uri))
        except:
            return False
        Channel.__run_channel_async()
        return True

    @staticmethod
    async def __connect(uri):
        Channel.socket = await websockets.connect(uri)

    @staticmethod
    def receive_now() -> str:
        return Channel.socket.recv()

    # vvv async tools vvv

    @staticmethod
    def __run_channel_async():
        def send_loop():
            Channel.__dequeue_loop(Channel.__data_to_send, Channel.__send)
        Channel.sender_thread = Thread(target=send_loop)
        Channel.sender_thread.start()

        def receive_loop():
            Channel.__dequeue_loop(Channel.__receive_handlers, Channel.__receive)
        Channel.receiver_thread = Thread(target=receive_loop)
        Channel.receiver_thread.start()

    __data_to_send = Queue()
    __receive_handlers = Queue()

    @staticmethod
    def __dequeue_loop(queue: Queue, item_handler):
        while True:
            while queue.empty():
                time.sleep(1 / Channel.priority)
            item = queue.get()
            item_handler(item)

    @staticmethod
    def __send(data: str):
        Channel.socket.send(data)

    @staticmethod
    def __receive(receive_handler):
        receive_handler(Channel.socket.recv())

    @staticmethod
    def send(data: str):
        if not isinstance(data, str):
            raise exceptions.ArgumentTypeException()
        Channel.__data_to_send.put(data)

    @staticmethod
    def receive_async(receive_handler):
        if type(receive_handler).__name__ != "function":
            raise exceptions.ArgumentTypeException()
        Channel.__receive_handlers.put(receive_handler)
