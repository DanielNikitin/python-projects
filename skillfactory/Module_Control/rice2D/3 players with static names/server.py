import socket
from _thread import *
from player import Player
import pickle

server = "localhost"
port = 10000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(5)
print("Waiting for a connection, Server Started")


players = [Player(0,0,50,50,(255,0,0), "123"),
           Player(100,100, 50,50, (0,0,255), "456"),
           Player(200, 200, 50, 50, (0, 255, 0), "789")]

def threaded_client(conn, player):
    conn.send(pickle.dumps(players[player]))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            players[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                reply = players

                #print("Received: ", data)
                #print("Sending : ", reply)

            conn.sendall(pickle.dumps(reply))
        except:
            break

    print(f"Disconnected")
    conn.close()

currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    print(f"info: {conn, currentPlayer}")
    currentPlayer += 1