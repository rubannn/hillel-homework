import asyncio

CHAT_USERS = set()
HOST = '127.0.0.1'
PORT = 1717


async def handle_echo(reader, writer):
    CHAT_USERS.add(writer)
    address = writer.get_extra_info('peername')
    print(f'Client {address} connected!')
    while True:
        data = await reader.read(1024)
        print(f'\t<client message>: {data.decode()}')
        if not data:
            print(f'Client {address} disconnected!')
            CHAT_USERS.remove(writer)
            writer.close()
            break

        for c_user in CHAT_USERS:
            if c_user != writer:
                c_user.write(data)
        await asyncio.gather(*(c_user.drain() for c_user in CHAT_USERS if c_user != writer))  # noqa


async def main():
    server = await asyncio.start_server(handle_echo, HOST, PORT)
    address = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Start server on [{address}]')

    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(main())
