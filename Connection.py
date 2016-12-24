import logging
import struct
import pickle
from curio.socket import *
from Message import Message


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('Connection')

class Connection:
	"""
	Initialize connection to computer
	implement base methods for data transfer
	"""
	@classmethod
	async def create_connection(cls, name, addr, client=None):
		"""
		Initialize connection by socket or address
		"""
		self = Connection()
		self.name = name
		self.addr = addr
		# If direct socket is't given
		if not client:
			self.client = socket(AF_INET, SOCK_STREAM)
			await self.client.connect(addr)
			# Create connection by address
		else:
			self.client = client
		logger.debug("Connection with {} initializes: {}:{}".format(self.name, *self.addr))
		return self


	async def receive_message(self):
		"""
		Receive message with such protocol:
		message -> length:data
		"""
		# Receive length of message
		raw_length = await self.client.recv(4)
		length = struct.unpack('>I', raw_length)[0]
		data = b''
		# Read until all data pi pieces
		while len(data) != length:
			packet = await self.client.recv(length - len(data))
			if not packet:
				logger.debug("Receive bad message from {}:{}".format(*self.addr))
				return None
			data += packet
		logger.debug("Receive message from {}:{}".format(*self.addr))
		print(type(pickle.loads(data)))
		return pickle.loads(data)
	

	async def send_message(self, data):
		"""
		Create message from raw data and send to the client
		message -> (len(data):data)
		"""
		print(type(data))
		data = pickle.dumps(data)
		try:
			message = struct.pack('>I', len(data)) + data
			await self._send_bytes(message)
		except KeyboardInterrupt:
			raise
		except:
			logger.debug("Error while creating message")
			pass
		logger.debug("Send message to {}:{}".format(*self.addr))


	async def _send_bytes(self, data):
		"""
		Handle sending data, if not all data was send
		repeat cycle again trying to send rest of the data
		"""
		data = data
		send = 0
		send += await self.client.send(data)
		while len(data) - send != 0:
			send += await self.s.send(data[send:])


	def close(self):
		self.sock.close()
		logger.debug("Connection closed with {}:{}".format(*self.addr))
