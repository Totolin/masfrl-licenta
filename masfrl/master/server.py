"""
    MASFRL-Server class.
    Opens socket listener, holds all MASFRL-Client connections, distributes
    work based on number of clients, assembles back work.
"""

import logging
import coloredlogs
import numpy as np
from threading import Thread
import utils.io as io

from connection.manager import ConnectionManager
from masfrl.messages import server as messages
from masfrl.engine.generator import generate_qlearn
from masfrl.engine.learner import Learner, leaner_algs
from masfrl.engine.splitter import split_environment
from utils.keyboard import listen_for_enter
from masfrl.engine.world import unstringify


# Use module logger
logger = logging.getLogger(__name__)

# Set logger for the whole module
coloredlogs.DEFAULT_LOG_FORMAT = '%(asctime)s.%(msecs)03d %(levelname)8s %(message)s'
coloredlogs.install(level='DEBUG')


class Server:
    def __init__(self, host, port):
        """
        Constructor for the MASFRL-Server class
        Starts a socket listener on given host and port
        Waits for connections based on given number
        Distributes work, assembles back once agents are done.
        :param host: host address to listen on
        :param port: port to listen on
        """
        logger.debug('Creating server instance')

        # Create a connection manager
        self.connection_manager = ConnectionManager(host, port)

        # Listen to desired port
        self.connection_manager.start_listening(1)

    def run(self, expected_clients=0, env_dict=None, algorithm=None, write_env=False):
        """
        Run MASFRL-Server instance, using given parameters.
        :param algorithm: Selected algorithm for the run
        :param expected_clients: Number of clients to wait for
        :param env_dict: Given environment to distribute
        :param write_env: Save generated environment
        :return: 
        """
        # Create environment for clients to work on
        if not env_dict:
            environment = generate_qlearn()
        else:
            environment = unstringify(env_dict)

        # Select algorithm that agents will run on:
        if not algorithm:
            algorithm = np.random.choice(leaner_algs)

        # Save it if it's required
        if write_env:
            io.save_env(environment)

        if expected_clients == 0:
            # Work alone
            learner = Learner(environment, True)
            learner.start(algorithm)

        else:
            # Wait for all of our clients
            result = self.connection_manager.wait_for_connections(expected_clients)

            if result:
                # Grab clients map
                clients = self.connection_manager.clients

                # Split environment to number of agents
                split_env = split_environment(environment, expected_clients)

                env_index = 0
                for client_address in clients:
                    # Select client's share of the algorithm
                    clients[client_address]['work'] = split_env[env_index]
                    env_index += 1

                    # Create standard work message
                    message = messages['work']
                    message['content'] = {
                        "environment": clients[client_address]['work'],
                        "algorithm": algorithm
                    }

                    # Send work to client
                    self.connection_manager.send_message(client_address, message)

                logger.info('All clients informed, waiting for keypress')

                # Listen for a keypress (specifically, Enter key)
                listen_for_enter()

                # Create learner to resume work
                learner = Learner(environment, False)

                # Request info back from clients
                best_score = 0
                for client_address in clients:
                    message = messages['request_work']

                    # Send request_work to client
                    self.connection_manager.send_message(client_address, message)

                    # Expect work back
                    response = self.connection_manager.receive_message(client_address)

                    # Reposition player to last successful position
                    if response['content']['successful']:
                        if response['content']['score'] > best_score:
                            best_score = response['content']['score']
                            learner.import_learner(response['content'])
                            logger.info('Importing learner by client %s ' % str(client_address))

                    learner.import_work(response['content']['Q'])

                learner.environment.log = False
                logger.warn('Merging work...')
                thread = Thread(target=learner.start, args=(algorithm,))
                thread.start()

                # Listen for a key to start showing the display
                listen_for_enter()

                # Stop the learner
                learner.stop()
                thread.join()

                # Show display, and resume
                learner.environment.log = True
                learner.set_show_display(True)
                learner.update_display()
                learner.start(algorithm)
