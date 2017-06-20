from connection.socket_connection import SocketConnection
from masfrl.engine.learner import Learner
from masfrl.engine.generator import generate_qlearn
from masfrl.engine.world import unstringify
from masfrl.messages import client as messages


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

        # Send ACK
        self.connection.send_message(messages['request_work'])

        env = unstringify(message['content'])
        learn = Learner(env, True)
        learn.start()
