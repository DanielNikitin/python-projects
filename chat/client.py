import socket
import sys

HEADER_LENGHT = 10
SERVER = ("localhost", 10000)

username = input("Your name: ").encode('UTF-8')  # закодированная байтовая строка

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(SERVER)
s.setblocking(0)

header = f"{len(username):<{HEADER_LENGHT}}".encode('UTF-8')  #
s.send(header+username)  # отправляем header сообщение с username

while 1:
    print('Please write a message: ')
    msg = input().encode('UTF-8')
    if msg:
        msg_header = f"{len(msg):<{HEADER_LENGHT}}".encode('UTF-8')
        s.send(msg_header + msg)
        print(msg_header, msg)

        try:
            user_header = s.recv(HEADER_LENGHT)  #
            if not len(user_header):
                sys.exit()
            user_length = int(user_header.decode('UTF-8').strip())  # убираем лишние отступы из заголовка
            username = s.recv(user_length)  # длинна username

            msg_header = s.recv(HEADER_LENGHT)
            msg_length = int(msg_header.decode('UTF-8').strip())

            data = s.recv(msg_length).decode('UTF-8')  # декодируем сообщение
            print(f"{username.decode('UTF-8')} - {data}")  # выводим его на экран
        except IOError as _ex:
            pass