import sys
import threading
from connection.socket_connection import SocketConnection
from masfrl.engine.learner import Learner
from masfrl.engine.world import unstringify
from masfrl.messages import client


class Client:
    def __init__(self, host, port):
        # Open a socket connection to the server
        self.connection = SocketConnection(host, port)

        # Connect to the server
        self.connection.connect()

        # Learner
        self.learner = None
        self.learner_thread = None

    def send_work(self):
        # Receive notification from server to send work back
        self.connection.receive_message()

        message = client['send_work']
        message['content'] = self.learner.Q
        self.connection.send_message(message)
        sys.exit(0)

    def work(self):
        # Inform server we need work
        message = self.connection.receive_message()

        # Create learner using received environment
        env = unstringify(message['content'])
        self.learner = Learner(env, True)

        # Run learner on separate thread
        self.learner_thread = threading.Thread(target=self.learner.start)
        self.learner_thread.daemon = True
        self.learner_thread.start()

        # Wait for send work message
        self.send_work()
