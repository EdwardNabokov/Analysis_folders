import asyncio
import logging
import threading

import janus

from Connection import Connection
from analysis.Analyzer import Analyzer

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('handler')


class ConnectionHandler:
    """
    Create connection with computer and run
    continuous process of listening and receiving data
    """
    @classmethod
    async def runHandler(cls, loop, addr, path, client=None):
        logger.info("Start connection handler")
        self = ConnectionHandler()
        self.loop = loop
        self.addr = addr
        self.connection = await Connection.create_connection(loop, addr, client)

        # Queues keep received messages and messages to send
        self.send = janus.Queue(loop=self.loop)
        self.receive = janus.Queue(loop=self.loop)

        # Path to button_connection folder
        self.path = path
        # Run analyzer
        analyzer = Analyzer(path, self.receive.sync_q, self.send.sync_q)
        threading.Thread(target=analyzer.run).start()

        # Continuos listening and receiving packages
        asyncio.ensure_future(self.listenHandler())
        asyncio.ensure_future(self.sendHandler())

        return self


    async def listenHandler(self):
        """
        Listen for comming messages and
        put them to the queue
        """
        logger.info("Listen handler started")
        while True:
            package = await self.connection.receive_message()
            # print('Receive: ', package)
            await self.receive.async_q.put(package)

    async def sendHandler(self):
        """
        Take messages from queue and
        send them
        """
        logger.info("Send handler started")
        while True:
            item = await self.send.async_q.get()
            if item:
                # print('Send: ', item)
                await self.connection.send_message(item)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    coro = loop.create_task(ConnectionHandler.runHandler(loop, ('172.1.1.121', 62252), '/Users/Alexander/Google/'))
    server = loop.run_until_complete(coro)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print('Closing connection')
    loop.close() 