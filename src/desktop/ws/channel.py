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
        uri = f"ws://{ip}:{port}/ws"
        try:
            asyncio.get_event_loop().run_until_complete(Channel.__connect(uri))
        except:
            return False
        Channel.__run_channel_async()
        return True

    @staticmethod
    async def __connect(uri):
        async with websockets.connect(uri) as ws:
            Channel.socket = ws

    @staticmethod
    def receive_now() -> str:
        return Channel.socket.recv()

    # vvv async tools vvv

    @staticmethod
    def __run_channel_async():
        Channel.sender_thread = Thread(target=Channel.__dequeue_loop(Channel.data_to_send, Channel.__send))
        Channel.receiver_thread = Thread(target=Channel.__dequeue_loop(Channel.lists_for_receive, Channel.__receive))
        Channel.sender_thread.start()
        Channel.receiver_thread.start()

    data_to_send = Queue()
    lists_for_receive = Queue()

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
    def __receive(received_data: list):
        received_data.append(Channel.socket.recv())

    @staticmethod
    def send(data: str):
        if not isinstance(data, str):
            raise exceptions.ArgumentTypeException()
        Channel.data_to_send.put(data)

    @staticmethod
    def receive_async(received_data: list):
        if not isinstance(received_data, list):
            raise exceptions.ArgumentTypeException()
        Channel.lists_for_receive.put(received_data)
