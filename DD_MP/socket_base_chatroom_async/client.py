import asyncio

HEADER_LENGTH = 10
IP = 'localhost'
PORT = 10000

async def receive_messages(reader):
    while True:
        try:
            # Receive username header
            username_header = await reader.readexactly(HEADER_LENGTH)

            # If we received no data, server gracefully closed the connection
            if not username_header:
                print('Connection closed by the server')
                break

            # Convert header to int value
            username_length = int(username_header.decode('utf-8').strip())

            # Receive and decode username
            username = await reader.readexactly(username_length)
            username = username.decode('utf-8')

            # Receive message header
            message_header = await reader.readexactly(HEADER_LENGTH)

            # Convert header to int value
            message_length = int(message_header.decode('utf-8').strip())

            # Receive and decode message
            message = await reader.readexactly(message_length)
            message = message.decode('utf-8')

            # Print message
            print(f'{username} > {message}')

        except asyncio.IncompleteReadError:
            # Incomplete read, continue receiving
            continue

        except Exception as e:
            # Any other exception - something went wrong
            print(f'Error receiving message: {str(e)}')
            break

async def send_message(writer, message):
    try:
        # Encode message to bytes
        message = message.encode('utf-8')

        # Prepare message header and convert to bytes
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')

        # Send message header and message
        writer.write(message_header + message)
        await writer.drain()

    except Exception as e:
        # Something went wrong while sending the message
        print(f'Error sending message: {str(e)}')

async def start_chat():
    try:
        # Connect to the server
        reader, writer = await asyncio.open_connection(IP, PORT)

        # Send the username
        my_username = input("Username: ")
        username = my_username.encode('utf-8')
        username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
        writer.write(username_header + username)
        await writer.drain()

        # Start receiving messages
        receive_task = asyncio.create_task(receive_messages(reader))

        while True:
            # Wait for user to input a message
            message = input(f'{my_username} > ')

            if message:
                # Send the message
                await send_message(writer, message)

    except Exception as e:
        # Something went wrong
        print(f'Error: {str(e)}')

    finally:
        # Close the connection
        writer.close()
        await writer.wait_closed()

# Start the chat
asyncio.run(start_chat())
