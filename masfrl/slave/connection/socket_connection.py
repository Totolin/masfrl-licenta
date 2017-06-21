import socket
import logging
import masfrl.messages as messages

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

    def receive_message(self):
        logger.debug('Listening for message from server')
        # Assemble message, by receiving chunks
        message = ''
        while 1:
            # If current chunk is valid, concatenate
            data = self.sock.recv(1024)

            if data:
                message += data

            if messages.stream_stop(data):
                break

        logger.debug('Received message from server. Decoding')
        return messages.decode_message(message)

    def send_message(self, message):
        logger.debug('Sending message to server')

        # Encode message
        message = messages.encode_message(message)

        # Send message to server
        self.sock.sendall(message)
