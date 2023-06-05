import socket
from _thread import *
import _pickle as pickle
import time
import random
import math

# Set constants
SERVER_IP = 'localhost'
PORT = 10000

# Создание сокета
S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
S.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
S.setblocking(False)

W, H = 1600, 830

START_RADIUS = 7

# try to connect to server
try:
	S.bind((SERVER_IP, PORT))
except socket.error as e:
	print(str(e))
	print("[SERVER] Server could not start")
	quit()

S.listen()  # listen for connections

print(f"[SERVER] Server Started with ip: {SERVER_IP}")

# dynamic variables
players = {}
connections = 0
_id = 0
colors = [(255,0,0), (255, 128, 0), (255,255,0),
		  (128,255,0),(0,255,0),(0,255,128),(0,255,255),
		  (0, 128, 255), (0,0,255), (0,0,255), (128,0,255),
		  (255,0,255), (255,0,128),(128,128,128), (0,0,0)]
start = False
stat_time = 0
game_time = "Starting Soon"

def get_start_location(players):
	while True:
		x = random.randrange(0,W)
		y = random.randrange(0,H)
	#return x, y

def threaded_client(conn, _id):
	global connections, players, balls, game_time, nxt, start

	current_id = _id

	# recieve a name from the client
	data = conn.recv(16)
	name = data.decode("utf-8")
	print("[LOG]", name, "connected to the server.")

	# Setup properties for each new player
	color = colors[current_id]
	x, y = get_start_location(players)
	players[current_id] = {"x":x, "y":y,"color":color,"score":0,"name":name}  # x, y color, score, name

	# pickle data and send initial info to clients
	conn.send(str.encode(str(current_id)))

	# server will recieve basic commands from client
	# it will send back all of the other clients info
	'''
	commands start with:
	move
	jump
	get
	id - returns id of client
	'''
	while True:
		try:
			# Recieve data from client
			data = conn.recv(32)

			if not data:
				break

			data = data.decode("utf-8")
			#print("[DATA] Recieved", data, "from client id:", current_id)

			# look for specific commands from recieved data
			if data.split(" ")[0] == "move":
				split_data = data.split(" ")
				x = int(split_data[1])
				y = int(split_data[2])
				players[current_id]["x"] = x
				players[current_id]["y"] = y

			elif data.split(" ")[0] == "id":
				send_data = str.encode(str(current_id))  # if user requests id then send it

			elif data.split(" ")[0] == "jump":
				send_data = pickle.dumps((balls,players, game_time))
			else:
				# any other command just send back list of players
				send_data = pickle.dumps((balls,players, game_time))

			# send data back to clients
			conn.send(send_data)

		except Exception as e:
			print(e)
			break  # if an exception has been reached disconnect client

		time.sleep(0.001)

	# When user disconnects
	print("[DISCONNECT] Name:", name, ", Client Id:", current_id, "disconnected")

	connections -= 1
	del players[current_id]  # remove client information from players list
	conn.close()  # close connection

# MAINLOOP

# Keep looping to accept new connections
print("[SERVER] Waiting for connections")
while True:

	host, addr = S.accept()
	print("[CONNECTION] Connected to: 1111", addr)

	# start game when a client on the server computer connects
	if addr[0] == SERVER_IP and not start:
		start = True
		start_time = time.time()
		print("[STARTED] Game Started")

	# increment connections start new thread then increment ids
	connections += 1
	start_new_thread(threaded_client, (host, _id))
	_id += 1
