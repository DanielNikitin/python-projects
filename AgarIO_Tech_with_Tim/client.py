import socket
import _pickle as pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(10.0)
        self.host = "localhost"
        self.port = 10000
        self.addr = (self.host, self.port)

    def connect(self, name):
        self.client.connect(self.addr)
        self.client.send(str.encode(name))
        val = self.client.recv(8)
        print('connected')
        return int(val.decode()) # can be int because will be an int id

    def disconnect(self):
        self.client.close()

    def send(self, data, pick=False):
        """
        :param data: str
        :param pick: boolean if should pickle or not
        :return: str
        """
        try:
            if pick:
                self.client.send(pickle.dumps(data))
            else:
                self.client.send(str.encode(data))
            reply = self.client.recv(2048*4)
            try:
                reply = pickle.loads(reply)
            except Exception as e:
                print(e)
            return reply
        except socket.error as e:
            print(e)