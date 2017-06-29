"""
    Module that takes care of socket communication from/to MASFRL-Client 
    instances. Manages all clients, storing them by their credentials.
    
"""

import socket
import sys
import logging
import time
import masfrl.messages as messages

logger = logging.getLogger(__name__)


class ConnectionManager:
    def __init__(self, host, port):
        """
        Constructor for the ConnectionManager class.
        :param host: host address to listen on
        :param port: port to listen on
        """
        logger.debug('Creating a Connection Manager')

        # Save future clients in a map
        self.clients = {}

        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the port
        self.server_address = (host, port)

    def start_listening(self, max_connections=1):
        """
        Binds created address to socket, and stars listening
        for incoming connections.
        :param max_connections: maximum number of queued connections
        :return: 
        """
        try:
            # Bind address tuple to socket
            self.sock.bind(self.server_address)

            # Listen for incoming connections
            self.sock.listen(max_connections)

        except socket.error as err:
            # Listening to desired port failed
            logger.error(err)
            sys.exit(1)

        logger.info('Server started on %s' % (self.server_address,))

    def wait_for_connections(self, expected, timeout=1000):
        """
        Waits for expected number of clients
        :param expected: integer - number of expected clients
        :param timeout: maximum time to wait for clients
        :return: 
        """

        logger.info('Waiting for %s connections' % expected)
        start = time.time()

        while True:

            # Break if we exceeded timeout
            current = time.time()
            if current - start >= timeout:
                break

            # Wait for a connection
            connection, client_address = self.sock.accept()

            # Save connection
            self.clients[str(client_address)] = {
                "connection": connection,
                "work": None
            }

            logger.info('Received connection from %s' % str(client_address))

            if len(self.clients) == expected:
                logger.info('All clients connected')
                break

        return True if len(self.clients) == expected else False

    def send_message(self, client_address, message):
        """
        Sends a client defined by it's address a message
        :param client_address: MASFRL-Client address
        :param message: message to be encoded
        :return: 
        """
        encoded = messages.encode_message(message)
        self.clients[client_address]['connection'].send(encoded)
        logger.debug('Sent message to client %s' % client_address)

    def receive_message(self, client_address):
        """
        Waits for a client to send a message
        :param client_address: MASFRL-Client address
        :return: decoded message
        """
        logger.debug('Waiting for message from client %s' % client_address)
        # Grab connection object from our map
        connection = self.clients[client_address]['connection']
        message = ''

        while True:

            # Continuously receive chunks
            data = connection.recv(1024)

            if data:
                message += data

            if messages.stream_stop(data):
                break

        logger.debug('Received encoded message')
        return messages.decode_message(message)

