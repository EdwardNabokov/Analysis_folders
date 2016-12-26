import logging
import asyncio
import struct
from Message import Message

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('Connection')


class Connection:
    @classmethod
    async def create_connection(cls, loop, addr, client=None):
        """
        Initialize connection by transport or address
        """
        self = Connection()
        self.loop = loop
        self.addr = addr
        # If direct transport is't given
        if not client:
            self.reader, self.writer = await asyncio.open_connection(self.addr[0], self.addr[1], loop=self.loop)
        # Create connection by address
        else:
            self.reader, self.writer = client
        logger.debug("Connection with {}:{} initialized".format(*self.addr))
        return self

    @staticmethod
    def __create_message(message):
        """
        Code message to binary package
        :param message: Message object
        :return: binary data
        """
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
        message = Message('', '', '')

        message.command = await self._receive_part(4)
        message.meta = await self._receive_part(4)
        message.data = await self._receive_part(4)

        return message

    async def _receive_part(self, length):
        length = await self.reader.read(length)
        length = struct.unpack('>I', length)[0]
        data = b''
        # Read until all data pi pieces
        while len(data) != length:
            packet = await self.reader.read(length - len(data))
            if not packet:
                logger.debug("Receive bad message from {}:{}".format(*self.addr))
                return None
            data += packet
        return data

    async def send_message(self, message):
        """
        Create message from raw data and send to the client
        """
        data = self.__create_message(message)
        try:
            self.writer.write(data)
            await self.writer.drain()
        except Exception as e:
            logger.debug("Error while creating message")
            logger.error('Failed : ' + str(e))
            pass
        logger.debug("Send message to {}:{}".format(*self.addr))


