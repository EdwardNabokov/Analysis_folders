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
        Initialize connection by socket or address
        """
        self = Connection()
        self.loop = loop
        self.addr = addr
        # If direct socket is't given
        if not client:
            self.reader, self.writer = await asyncio.open_connection(self.addr[0], self.addr[1], loop=self.loop)
        # Create connection by address
        else:
            self.reader, self.writer = client
        logger.debug("Connection with {}:{} initialized".format(*self.addr))
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
        length = await self.reader.read(4)
        command_length = struct.unpack('>I', length)[0]

        data = b''
        # Read until all data pi pieces
        while len(data) != command_length:
            packet = await self.reader.read(command_length - len(data))
            if not packet:
                logger.debug("Receive bad message from {}:{}".format(*self.addr))
                return None
            data += packet
        m.command = data

        length = await self.reader.read(4)
        meta_length = struct.unpack('>I', length)[0]
        data = b''
        # Read until all data pi pieces
        while len(data) != meta_length:
            packet = await self.reader.read(meta_length - len(data))
            if not packet:
                logger.debug("Receive bad message from {}:{}".format(*self.addr))
                return None
            data += packet
        m.meta = data

        length = await self.reader.read(4)
        data_length = struct.unpack('>I', length)[0]
        data = b''
        # Read until all data pi pieces
        while len(data) != data_length:
            packet = await self.reader.read(data_length - len(data))
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
            self.writer.write(data)
            await self.writer.drain()
        except Exception as e:
            logger.debug("Error while creating message")
            logger.error('Failed : ' + str(e))
            pass
        logger.debug("Send message to {}:{}".format(*self.addr))


