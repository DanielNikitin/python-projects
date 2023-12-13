from client_network import Network

n = Network()
from_server = n.server_data()

meow = from_server.get("meow", [])
number = from_server.get("numbers", [])
player = from_server.get('player', {})

print(f"Client received data: \n{meow}\n{number}\n{player}")


shoot = {'x': '1', 'y': '2', 'mouse_btn': '1'}
n.send_data(shoot)
print(f"Client send to server :: {shoot}")

