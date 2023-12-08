import pickle
import socket

# Клиент
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 10000))

# Получение данных через сокет и их десериализация
received_data = client_socket.recv(1024)  # получили байты

loaded_data = pickle.loads(received_data)  # изменение формата в нормальный

print(loaded_data)

# Закрытие соединения
client_socket.close()