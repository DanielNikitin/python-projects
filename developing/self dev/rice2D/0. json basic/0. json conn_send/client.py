import pygame
import json
import time

from network import Network

def main():
    run = True
    network = Network()
    network.connect()

    try:
        while run:
            # -------- DATA TO SEND
            network.send_data({"action": "move_right"})

            # -------- RECEIVED DATA
            received_data = network.receive_data()

            if received_data is not None:
                print(received_data)

    except KeyboardInterrupt:
        pass
    finally:
        network.disconnect()


main()