import pickle
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 10000))
server_socket.listen(2)

print("Ждем подключения клиента...")
client_socket, address = server_socket.accept()
print(f"Подключено к {address}")

data_to_send = {'meow': 'Привет, клиент!', 'numbers': [1, 2, 3], 'player': 'x, y, width, height, id_1'}
serialized_data = pickle.dumps(data_to_send)
client_socket.send(serialized_data)
print(f"Sending to client :: {data_to_send}")

# Принимаем данные от клиента
print("SERVER: RECEIVED FROM CLIENT")
bytes_from_client = client_socket.recv(2048)
data_from_client = pickle.loads(bytes_from_client)
print(f"Data from client :: {data_from_client}")

x = data_from_client.get('x', [])
y = data_from_client.get('y', [])
mouse_btn = data_from_client.get('mouse_btn', [])
print(f"x: {x}\ny: {y}\nmouse_btn: {mouse_btn}")

# Закрытие соединения не трогаем, чтобы сервер продолжал слушать новые подключения
# client_socket.close()
# server_socket.close()