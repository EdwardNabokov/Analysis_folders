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

    def __create_message(self, message):
        msg_format = "!L{}sL{}sL{}s".format(message.command_size(), message.meta_size(), message.data_size())
        msg = struct.Struct(msg_format)
        msg = msg.pack(message.command_size(), message.command, message.meta_size(),
                       message.meta, message.data_size(), message.data)
        return msg

    async def receive_message(self):
        """
		Receive message with such protocol:
		command
		meta
		data
		"""
        m = Message('', '', '')
        # Receive length of command
        length = await self.client.recv(4)
        command_length = struct.unpack('>I', length)[0]

        data = b''
        # Read until all data pi pieces
        while len(data) != command_length:
            packet = await self.client.recv(command_length - len(data))
            if not packet:
                logger.debug("Receive bad message from {}:{}".format(*self.addr))
                return None
            data += packet
        m.command = data

        length = await self.client.recv(4)
        meta_length = struct.unpack('>I', length)[0]
        data = b''
        # Read until all data pi pieces
        while len(data) != meta_length:
            packet = await self.client.recv(meta_length - len(data))
            if not packet:
                logger.debug("Receive bad message from {}:{}".format(*self.addr))
                return None
            data += packet
        m.meta = data

        length = await self.client.recv(4)
        data_length = struct.unpack('>I', length)[0]
        data = b''
        # Read until all data pi pieces
        while len(data) != data_length:
            packet = await self.client.recv(data_length - len(data))
            if not packet:
                logger.debug("Receive bad message from {}:{}".format(*self.addr))
                return None
            data += packet
        m.data = data

        logger.debug("Receive message from {}:{}".format(*self.addr))
        return m

    async def send_message(self, message):
        """
		Create message from raw data and send to the client
		message -> (len(data):data)
		"""
        data = self.__create_message(message)
        try:
            await self._send_bytes(data)
        except KeyboardInterrupt:
            raise
        except Exception as e:
            logger.debug("Error while creating message")
            logger.error('Failed : ' + str(e))
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
            send += await self.client.send(data[send:])

    def close(self):
        self.sock.close()
        logger.debug("Connection closed with {}:{}".format(*self.addr))
