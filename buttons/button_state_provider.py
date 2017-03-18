import logging
import socket
import time

def get_logger():
    return logging.getLogger(__name__)

class ButtonStateProvider:

    def get_state(self):
        raise Exception("Must be overridden by superclass")

class SocketButtonStateProvider:

    def __init__(self, url, port):
        self.url = url
        self.port = port


    def wait_for_connection(self):
        while(True):
            try:
                resp = self.get_state()
                return
            except requests.exceptions.ConnectionError:
                time.sleep(1)

    def get_state(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.url, self.port))
        data = s.recv(6).decode("utf-8")
        return [state == '1' for state in data]
