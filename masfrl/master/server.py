import logging
import coloredlogs

from connection.manager import ConnectionManager
from masfrl.messages import server as messages
from masfrl.engine.generator import generate_qlearn
from masfrl.engine.world import stringify
from masfrl.engine.learner import Learner
from masfrl.engine.splitter import split_environment
from utils.keyboard import listen_for_enter

# Use module logger
logger = logging.getLogger(__name__)

# Set logger for the whole module
coloredlogs.DEFAULT_LOG_FORMAT = '%(asctime)s.%(msecs)03d %(levelname)8s %(message)s'
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

            # Create environment for them to work on
            environment = generate_qlearn()

            for client_address in clients:
                client_env = split_environment(environment, 1)
                message = messages['work']
                message['content'] = client_env

                # Send work to client
                self.connection_manager.send_message(client_address, message)

                # Wait for ack
                # response = self.connection_manager.receive_message(client_address)
                # print response

            logger.info('All clients informed, waiting for keypress')

            # Listen for a keypress (specifically, Enter key)
            listen_for_enter()

            # Create learner to resume work
            learner = Learner(environment, True)

            # Request info back from clients
            for client_address in clients:
                message = messages['request_work']

                # Send request_work to client
                self.connection_manager.send_message(client_address, message)

                # Expect work back
                response = self.connection_manager.receive_message(client_address)

                #learner.import_work(response['content'])

            learner.start()




