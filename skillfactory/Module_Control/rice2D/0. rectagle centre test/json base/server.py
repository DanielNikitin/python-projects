import json
import socket

# Сервер
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 10000))
server_socket.listen(2)

print("Ждем подключения клиента...")
client_socket, address = server_socket.accept()
print(f"Подключено к {address}")

# Отправка данных через сокет с использованием json
data_to_send = {'message': 'Привет, клиент!', 'numbers': [1, 2, 3]}

serialized_data = json.dumps(data_to_send).encode('utf-8')  # преобразуем в байты

client_socket.send(serialized_data)  # отправляем байты клиенту

# Закрытие соединения
client_socket.close()
server_socket.close()
