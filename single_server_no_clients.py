import sys
import masfrl.master.utils.io as io
from masfrl.master.server import Server
from masfrl.slave.client import Client

host = 'localhost'
port = 8000

# Read environment file
server = Server(host, port)
server.run(0, algorithm='qlearn')
