from connection.socket_connection import SocketConnection
from masfrl.engine.learner import Learner
from masfrl.engine.generator import generate_qlearn


class Client:
    def __init__(self, host, port):
        # Open a socket connection to the server
        self.connection = SocketConnection(host, port)

        # Connect to the server
        self.connection.connect()

    def work(self):
        # Inform server we need work
        message = self.connection.receive_message()

        print message

        env = generate_qlearn()
        learn = Learner(env, True)
        learn.start()
