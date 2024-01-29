import socket
import json

class Network:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = 'localhost'
        self.port = 10000
        self.server_address = (self.addr, self.port)

    def connect(self):
        try:
            self.client_socket.connect(self.server_address)
            print("NET: Connected to the server")
        except socket.error as e:
            print(f"NET: Error connecting to the server: {e}")

    def send_data(self, data):
        try:
            encoded_data = json.dumps(data).encode('utf-8')
            self.client_socket.send(encoded_data)
        except socket.error as e:
            print(f"NET: Error sending data: {e}")

    def receive_data(self):
        try:
            data = self.client_socket.recv(1024)
            decoded_data = json.loads(data.decode('utf-8'))
            #print(f"NET :: {decoded_data}")
            return decoded_data
        except socket.error as e:
            print(f"NET: Error receiving data: {e}")
            return None

    def disconnect(self):
        print("NET: Disconnected")
        self.client_socket.close()
