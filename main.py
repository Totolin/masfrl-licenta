import sys
from masfrl.master.server import Server
from masfrl.slave.client import Client


host = 'localhost'
port = 8000
if str(sys.argv[1]) == 'server':
    server = Server(host, port)
    server.run()
else:
    client = Client(host, port)
    client.work()

