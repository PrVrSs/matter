import asyncio


class SimpleClient:
    def __init__(self, loop=None):
        self._loop = loop or asyncio.get_running_loop()
        self._buffer = 1024
        self._reader = None
        self._writer = None
        self._timeout = 10.0

    async def create_connection(self, host: str = '0.0.0.0', port: int = 8888):
        self._reader, self._writer = await asyncio.open_connection(host, port)

    def send(self, data) -> None:
        self._writer.write(data.encode())

    async def read(self):
        while chunk := await self._reader.read(self._buffer):
            yield chunk

        self._writer.close()


async def main():
    c = SimpleClient()
    await c.create_connection()
    c.send('''''')

    async for data in c.read():
        print(data.decode())

if __name__ == '__main__':
    asyncio.run(main())


class BaseProtocol:
    pass


class TCPProtocol(BaseProtocol):
    pass


class HTTPProtocol(BaseProtocol):
    pass
