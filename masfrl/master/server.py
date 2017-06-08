import logging
import coloredlogs

from connection.manager import ConnectionManager
from masfrl.messages import server as messages

# Use module logger
logger = logging.getLogger(__name__)

# Set logger for the whole module
coloredlogs.DEFAULT_LOG_FORMAT = '%(levelname)8s %(message)s'
coloredlogs.install(level='DEBUG')


class Server:
    def __init__(self, host, port):
        logger.debug('Creating server instance')

        # Create a connection manager
        self.connection_manager = ConnectionManager(host, port)

        # Listen to desired port
        self.connection_manager.start_listening(1)

    def run(self, expected_clients=1):

        # Wait for all of our clients
        result = self.connection_manager.wait_for_connections(expected_clients)

        if result:
            # Grab clients map
            clients = self.connection_manager.clients

            for client_address in clients:
                self.connection_manager.send_message(client_address, messages['work'])