import asyncio


class Receiver(asyncio.Protocol):
    def data_received(self, data):
        print(data)


class Sender(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        print('connected')

    def data_received(self, data):
        print(data)


def main():
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(loop.create_server(Receiver, '127.0.0.1', 40000))
        loop.run_until_complete(loop.create_server(Sender, '127.0.0.1', 40001))
        loop.run_forever()
    except:
        loop.close()


if __name__ == '__main__':
    main()
