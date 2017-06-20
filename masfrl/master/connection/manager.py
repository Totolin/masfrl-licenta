import socket
import sys
import logging
import time
import masfrl.messages as messages

logger = logging.getLogger(__name__)


class ConnectionManager:
    def __init__(self, host, port):

        logger.debug('Creating a Connection Manager')

        # Save future clients in a map
        self.clients = {}

        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the port
        self.server_address = (host, port)

    def start_listening(self, max_connections=1):
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
            self.clients[str(client_address)] = connection

            logger.info('Received connection from %s' % str(client_address))

            if len(self.clients) == expected:
                logger.info('All clients connected')
                break

        return True if len(self.clients) == expected else False

    def send_message(self, client_address, message):
        encoded = messages.encode_message(message)
        self.clients[client_address].send(encoded)
        logger.debug('Sent message to client %s' % client_address)

    def receive_message(self, client_address):
        logger.debug('Waiting for message from client %s' % client_address)
        # Grab connection object from our map
        connection = self.clients[client_address]
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

