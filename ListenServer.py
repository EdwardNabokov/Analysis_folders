import asyncio
import logging
from ConnectionHandler import ConnectionHandler

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('server')


class ListenServer:

    def __init__(self, loop, path):
        logger.info("Start listening server")
        self.loop = loop
        self.path = path

    def start(self, reader, writer):
        addr = writer.get_extra_info('peername')
        asyncio.ensure_future(self.runHandler(addr, (reader, writer)))

    async def runHandler(self, addr, transport):
        connection = ConnectionHandler()
        await connection.runHandler(self.loop, addr, self.path, transport)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    a = ListenServer(loop, '/Users/Alexander/Google/')
    coro = asyncio.start_server(a.start, '0.0.0.0', 7866, loop=loop)
    server = loop.run_until_complete(coro)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print('Closing connection')
    loop.close()