from channels.generic.websocket import WebsocketConsumer


class WebsocketRequestHandler(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        # echo
        if text_data is not None:
            text_data = text_data[::-1]
        if bytes_data is not None:
            bytes_data = bytes_data[::-1]
        self.send(text_data=text_data, bytes_data=bytes_data)
