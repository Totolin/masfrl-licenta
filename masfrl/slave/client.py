from connection.socket_connection import SocketConnection

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
