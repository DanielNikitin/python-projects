import json
import socket

# Клиент
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 10000))

# Получение данных через сокет с использованием json
received_data = client_socket.recv(1024).decode('utf-8')
parsed_data = json.loads(received_data)

print(f"Получено от сервера: {parsed_data}")

# Закрытие соединения
client_socket.close()
