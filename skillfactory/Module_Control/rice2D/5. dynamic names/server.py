import socket
from _thread import *
from player import Player
import pickle
import random

server = "localhost"
port = 10000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen(5)
print("Waiting for a connection, Server Started")

players = {}
connections = 0
_id = 0

colors = [(255,0,0),
		  (255, 128, 0),
		  (255,255,0),
		  (128,255,0),
		  (0,255,0),
		  (0,255,128),
		  (0,255,255),
		  (0, 128, 255),
		  (0,0,255),
		  (0,0,255),
		  (128,0,255),
		  (255,0,255),
		  (255,0,128),
		  (128,128,128),
		  (0,0,0)]

def player_respawn(players):
        x = 50
        y = 50
        for player in players:
            p = players[player]


def threaded_client(conn, player):
    conn.send(pickle.dumps(players[player]))
    reply = ""

    current_id = _id

    while True:
        try:
            data = pickle.loads(conn.recv(2048))  #
            players[player] = data  #
            name = data.decode("utf-8")
            print(f"** {name} **")

            # Setup properties for each new player
            #color = colors[current_id]
            #x, y = player_respawn(players)
            #players[current_id] = {"x": x, "y": y, "color": color, "name": name}  # x, y, color, name

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
    print("Connected:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1