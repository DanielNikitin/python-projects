import socket
import threading
import json
import time

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 5555))
server.listen()

clients = []
game_state = {'player_pos': (50, 50)}

def handle_client(client_socket, addr):
    global game_state

    # Отправка приветственного сообщения
    welcome_message = {'action': 'welcome', 'data': 'You are connected to the server!'}
    client_socket.send(json.dumps(welcome_message).encode('utf-8'))

    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break

            message = json.loads(data.decode('utf-8'))

            if 'action' in message:
                if message['action'] == 'move':
                    game_state['player_pos'] = message['data']

        except Exception as e:
            print(f"Error handling client {addr}: {str(e)}")
            break

    clients.remove((client_socket, addr))
    client_socket.close()

def send_game_state():
    global game_state
    while True:
        time.sleep(0.1)
        for client_socket, addr in clients:
            try:
                client_socket.send(json.dumps(game_state).encode('utf-8'))
            except Exception as e:
                print(f"Error sending game state to {addr}: {str(e)}")

send_thread = threading.Thread(target=send_game_state)
send_thread.start()

print("Server is running and listening on port 5555. Ready to accept clients.")

while True:
    client_socket, addr = server.accept()
    clients.append((client_socket, addr))

    client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
    client_thread.start()
