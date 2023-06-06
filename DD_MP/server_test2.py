import socket
import threading
import pygame
import time
import pickle

class Server:
    def __init__(self, ip, port):
        print("[SERVER] Configuring Server...")
        time.sleep(0.5)
        self.ip = ip
        self.port = port

        self.running = False

        pygame.init()

        #self.screen = pygame.display.set_mode((200, 200))

        #self.clock = pygame.time.Clock()
        #self.FPS = 30

        # Socket Config
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.server.setblocking(False)

        # Constants
        self.all_players = {}
        self._id = 0

        # Run Server Thread
        self.lock = threading.Lock()
        threading.Thread(target=self.run_server).start()

    def run_server(self):
        try:
            self.server.bind((self.ip, self.port))
            self.server.listen()
            print(f"[SERVER] Server started with IP: {self.ip, self.port}")
            self.running = True
            print("[SERVER] Activating Connect_Handler Function")
            time.sleep(0.5)
            threading.Thread(target=self.connect_handler, args=(client)).start()

        except socket.error as e:
            print(str(e))
            print("[SERVER] Server could not start")
            quit()

    def connect_handler(self, client):

        listening_message = True
        data = client.recv(16)
        name = data.decode("utf-8")

        while self.running:
            # Listening connections
            try:
                client, address = self.server.accept()
                data = client.recv(32)
                with self.lock:
                    if client not in self.all_players:
                        self._id += 1
                        self.all_players[client] = self._id
                        client.send(str(self._id).encode('utf-8'))
                        print("[LOG]", self._id, name, "connected to the server")
            except:
                if listening_message:
                    print("[SERVER] Listening for Connections")
                    listening_message = False
                pass

            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("[SERVER] Shutting Down")
                    self.running = False
                    quit()
            time.sleep(0.001)

        # When user disconnects
        print("[DISCONNECT] Name:", name, "ID:", self._id, "disconnected")

        self._id -= 1
        del self.all_players[client]
        client.close()  # close connection

start_server_var = Server('127.0.0.1', 10000)