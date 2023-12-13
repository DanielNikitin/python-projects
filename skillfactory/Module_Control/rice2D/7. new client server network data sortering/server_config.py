
import socket

WIDHT_SERVER_WINDOW, HEIGHT_SERVER_ROOM = 300, 300  # серверное окно

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

server_ip = "localhost"
port = 10000