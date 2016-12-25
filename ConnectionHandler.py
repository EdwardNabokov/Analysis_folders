import curio
import threading
import time
import logging
import pickle
from queue import Queue
from Connection import Connection
from CommandHandler import CommandHandler
from Analyzer import Analyzer

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('handler')


class ConnectionHandler:
    """
	Create connection with computer and run
	continuous process of listening and receiving data
	"""

    @classmethod
    async def runHandler(cls, name, addr, path, client=None):
        logger.debug("Start connection handler")
        self = ConnectionHandler()
        self.name = name
        self.connection = await Connection.create_connection(name, addr, client)

        # Queues keep received messages and messages to send
        self.send = Queue()
        self.receive = Queue()
        # Path to sync folder
        self.path = path
        # Run analyzer
        analyzer = Analyzer(path, self.receive, self.send)
        threading.Thread(target=analyzer.run).start()

        # Continuos listening and receiving packages
        await curio.spawn(self.listenHandler())
        await curio.spawn(self.sendHandler())

        return self

    async def listenHandler(self):
        """
		Listen for comming messages and 
		put them to the queue
		"""
        logger.debug("Listen handler started")
        while True:
            package = await self.connection.receive_message()
            print('Receive: ', package)
            self.receive.put(package)
            print('put message')

    async def sendHandler(self):
        """
		Take messages from queue and 
		send them
		"""
        logger.debug("Send handler started")
        while True:
            item = await curio.abide(self.send.get)
            if item:
                print('Send: ', item)
                await curio.sleep(0.1)
                await self.connection.send_message(item)


if __name__ == '__main__':
    curio.run(
        ConnectionHandler.runHandler('new_connection', ('172.1.1.120', 55592), '/Users/Alexander/Google/'))
