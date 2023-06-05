import socket
import threading
import pygame
import time


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
        self.players = {}

        # Run Server Thread
        threading.Thread(target=self.run_server()).start()

    def run_server(self):
        try:
            self.server.bind((self.ip, self.port))
            self.server.listen()
            print(f"[SERVER] Server started with IP: {self.ip, self.port}")
            self.running = True
            print("[SERVER] Activating Connect_Handler Function")
            threading.Thread(target=self.connect_handler()).start()
        except socket.error as e:
            print(str(e))
            print("[SERVER] Server could not start")
            quit()

    def connect_handler(self):
        while self.running:
            print("connect handler is started")
            time.sleep(1)

            # -----ОБРАБОТЧИК СОБЫТИЙ-----
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("[SERVER] Shutting Down")
                    self.running = False
                    quit()


start_server_var = Server('127.0.0.1', 10000)