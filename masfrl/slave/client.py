import sys
import threading
from connection.socket_connection import SocketConnection
from masfrl.engine.learner import Learner
from masfrl.engine.world import unstringify
from masfrl.messages import client


class Client:
    def __init__(self, host, port, run_display=True):
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
        # Receive notification from server to send work back
        self.connection.receive_message()

        # Compose return message
        message = client['send_work']
        message['content'] = {
            "Q": self.learner.Q,
            "player": self.learner.environment.get_orig_player(),
            "successful": self.learner.environment.successful
        }

        # Send back to server
        self.connection.send_message(message)

        # Message received, stop learner
        self.learner.stop()

    def work(self):
        # Inform server we need work
        message = self.connection.receive_message()

        # Create learner using received environment
        env = unstringify(message['content'])
        self.learner = Learner(env, self.run_display)

        # Listen for a message on a separate thread
        self.worker_thread = threading.Thread(target=self.send_work)
        self.worker_thread.daemon = True
        self.worker_thread.start()

        # Run learner on main thread
        self.learner.start()

        # Exit script
        sys.exit(0)
