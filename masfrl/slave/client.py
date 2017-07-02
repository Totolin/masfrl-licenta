"""
    MASFRL-Client class.
    Holds all communication and work means that a distributed agent
    needs. Communicates with the server using given parameters.
"""

import sys
import threading
from connection.socket_connection import SocketConnection
from masfrl.engine.learner import Learner
from masfrl.engine.world import unstringify
from masfrl.messages import client


class Client:
    def __init__(self, host, port, run_display=True):
        """
        Constructor for the MASFRL-Client class.
        :param host: address of the MASFRL-Server instance (Master)
        :param port: port of the MASFRL-Server instance
        :param run_display: True if display driver should show the work running
                            This will slow down the execution.
        """
        # Open a socket connection to the server
        self.connection = SocketConnection(host, port)

        # Connect to the server
        self.connection.connect()

        # Learner
        self.learner = None
        self.worker_thread = None

        # Display flag
        self.run_display = run_display

    def send_work(self):
        """
        Sends work back to MASFRL-Server.
        Should be executed only after MASFRL-Server asked for work.
        :return: 
        """
        # Receive notification from server to send work back
        self.connection.receive_message()

        # Compose return message
        message = client['send_work']
        message['content'] = self.learner.to_string()

        # Send back to server
        self.connection.send_message(message)

        # Message received, stop learner
        self.learner.stop()

    def work(self):
        """
        Starts listening for a work message from MASFRL-Server.
        Once received, will start running chosen RL algorithm on given
        environment.
        :return: 
        """
        # Inform server we need work
        message = self.connection.receive_message()

        # Create learner using received environment
        env = unstringify(message['content']['environment'])
        algorithm = message['content']['algorithm']
        self.learner = Learner(env, self.run_display)

        # Listen for a message on a separate thread
        self.worker_thread = threading.Thread(target=self.send_work)
        self.worker_thread.daemon = True
        self.worker_thread.start()

        # Run learner on main thread
        self.learner.start(algorithm)

        # Exit script
        sys.exit(0)
