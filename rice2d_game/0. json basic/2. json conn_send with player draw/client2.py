import socket
import json

def send_data(client_socket, data):
    encoded_data = json.dumps(data).encode('utf-8')
    client_socket.send(encoded_data)

if __name__ == "__main__":
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 5555))

    try:
        while True:
            message = input("Enter a message to send to the server (type 'exit' to quit): ")
            if message.lower() == 'exit':
                break
            send_data(client_socket, message)
    except KeyboardInterrupt:
        pass
    finally:
        client_socket.close()
