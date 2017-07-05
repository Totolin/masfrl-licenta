import sys
import masfrl.master.utils.io as io
from masfrl.master.server import Server
from masfrl.slave.client import Client

host = 'localhost'
port = 8000

if str(sys.argv[1]) == 'server':
    # Read environment file
    server = Server(host, port)
    server.run(3, algorithm='qlearn')
else:
    client = Client(host, port, True)
    client.work()
