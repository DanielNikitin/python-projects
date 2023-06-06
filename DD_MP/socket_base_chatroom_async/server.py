import asyncio

HEADER_LENGTH = 10
IP = 'localhost'
PORT = 10000

clients = {}

async def handle_client(client_reader, client_writer):
    user = await receive_message(client_reader)
    if user is False:
        return

    clients[client_writer] = user

    print(f"Accepted new connection from {client_writer.get_extra_info('peername')} username:{user['data'].decode('utf-8')}")

    while True:
        message = await receive_message(client_reader)

        if message is False:
            print(f"Close connection from {clients[client_writer]['data'].decode('utf-8')}")
            del clients[client_writer]
            break

        user = clients[client_writer]

        print(f"Received message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")

        for client_writer in clients:
            if client_writer != client_writer:
                await send_message(client_writer, user, message)

    client_writer.close()

async def receive_message(client_reader):
    try:
        message_header = await client_reader.readexactly(HEADER_LENGTH)

        if not message_header:
            return False

        message_length = int(message_header.decode("utf-8").strip())
        message_data = await client_reader.readexactly(message_length)
        return {"header": message_header, "data": message_data}
    except asyncio.IncompleteReadError:
        return False

async def send_message(client_writer, user, message):
    try:
        client_writer.write(user['header'] + user['data'] + message['header'] + message['data'])
        await client_writer.drain()
    except asyncio.CancelledError:
        pass

async def start_server():
    server = await asyncio.start_server(
        handle_client,
        IP,
        PORT
    )

    print(f"Server started on {IP}:{PORT}")

    async with server:
        await server.serve_forever()

asyncio.run(start_server())
