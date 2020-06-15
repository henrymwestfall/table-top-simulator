import socket
import pickle
import time

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "172.16.1.12" # For this to work on your machine this must be equal to the ipv4 address of the machine running the server
                                    # You can find this address by typing ipconfig in CMD and copying the ipv4 address. Again this must be the servers
                                    # ipv4 address. This field will be the same for all your clients.
        self.port = 5555
        self.addr = (self.host, self.port)
        self.id = self.connect()

    def connect(self):
        self.client.connect(self.addr)
        return pickle.loads(self.client.recv(2048))

    def send(self, data):
        """
        :param data: str
        :return: str
        """
        try:
            self.client.send(pickle.dumps(data))
            try:
                reply = pickle.loads(self.client.recv(20480))
            except EOFError:
                reply = None
            return reply
        except socket.error as e:
            return str(e)
