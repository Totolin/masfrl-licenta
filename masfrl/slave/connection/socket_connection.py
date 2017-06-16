import socket
import logging

# Use module logger
logger = logging.getLogger(__name__)


class SocketConnection:
    def __init__(self, host, port):
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        self.server_address = (host, port)

    def connect(self):
        self.sock.connect(self.server_address)

    def encode_message(self, message):
        return str(message)

    def decode_message(self, message):
        return eval(message)

    def receive_message(self):

        # Assemble message, by receiving chunks
        message = ''
        while 1:
            # If current chunk is valid, concatenate
            data = self.sock.recv(1024)
            if not data:
                break
            message += data

        return self.decode_message(message)

    def send_message(self, message):
        logger.debug('Sending message to server: %s' % message)

        # Encode message
        message = self.encode_message(message)

        # Send message to server
        self.sock.sendall(message)
