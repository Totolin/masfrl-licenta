"""
    Module that takes care of communication from/to MASFRL-Server. 
    Offers send/receive methods, both which encode and decode messages
    automatically. Requires MASFRL-Server credentials to connect.
"""

import socket
import logging
import masfrl.messages as messages

# Use module logger
logger = logging.getLogger(__name__)


class SocketConnection:
    def __init__(self, host, port):
        """
        Constructor for the SocketConnection class.
        Creates a socket connection to the MASFRL-Server, based on
        the given parameters. Asynchronously holds the connection, without
        blocking thread that instantiated class.
        :param host: host address of MASFRL-Server
        :param port: port of the MASFRL-Server
        """
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        self.server_address = (host, port)

    def connect(self):
        """
        Calls connect on the created socket connection
        :return: 
        """
        self.sock.connect(self.server_address)

    def receive_message(self):
        """
        Listens for a message from the connected MASFRL-Server.
        :return: String representation of the decoded message
        """
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
        """
        Encodes a message, then sends it over the current socket connection
        :param message: String representation of the message 
        :return: 
        """
        logger.debug('Sending message to server')

        # Encode message
        message = messages.encode_message(message)

        # Send message to server
        self.sock.sendall(message)
