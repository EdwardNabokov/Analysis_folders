import curio
import logging
from curio import Queue
from curio.socket import *
from ConnectionHandler import ConnectionHandler

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('server')


class ListenServer:
	"""
	Create server that listen to connection and
	run handleConnection after connection made
	address: tuple (ip, port)
	"""
	def __init__(self, path):
		self.sock = socket(AF_INET, SOCK_STREAM)
		self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
		self.sock.bind(('127.0.0.1', 0))
		self.sock.listen(5)

		self.path = path

		logger.debug("Start listening server: {}:{}".format(*self.sock.getsockname()))
		print(self.sock.getsockname())

	async def start(self):
		"""
		Servers starts listen
		"""
		while True:
			self.client, self.addr = await self.sock.accept()

			# Create name of connection (ip,port)
			name = self.addr[0] + ':' + str(self.addr[1])

			# Redirect made connection to handler
			connection = ConnectionHandler()
			await curio.spawn(connection.runHandler(name, self.addr, self.path, self.client))


if __name__ == '__main__':
	server = ListenServer('/Users/Alexander/Project/')
	curio.run(server.start())