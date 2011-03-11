from timeit import default_timer as timer
from xmlrpc.client import ServerProxy

client = ServerProxy('http://localhost:10002')

    