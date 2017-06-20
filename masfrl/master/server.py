import logging
import coloredlogs
from pynput import keyboard

from connection.manager import ConnectionManager
from masfrl.messages import server as messages
from masfrl.engine.generator import generate_qlearn
from masfrl.engine.world import stringify
from masfrl.engine.splitter import split_environment

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

            for client_address in clients:
                # After splitting
                environment = generate_qlearn()
                client_env = split_environment(environment, 1)
                message = messages['work']
                message['content'] = stringify(client_env)

                # Send work to client
                self.connection_manager.send_message(client_address, message)

                # Wait for ack
                response = self.connection_manager.receive_message(client_address)
                print response

            logger.info('All clients informed, waiting for keypress')

            # def on_press(key):
            #     try:
            #         k = key.char  # single-char keys
            #     except:
            #         k = key.name  # other keys
            #     if key == keyboard.Key.esc: return False  # stop listener
            #     if k in ['1', '2', 'left', 'right']:  # keys interested
            #         # self.keys.append(k) # store it in global-like variable
            #         print('Key pressed: ' + k)
            #         return False  # remove this if want more keys
            #
            # lis = keyboard.Listener(on_press=on_press)
            # lis.start()  # start to listen on a separate thread
            # lis.join()  # no this if main thread is polling self.keys
