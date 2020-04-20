import socket

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        self.server = '2a02:4780:1:1::1:94bb'
        self.port = 42069
        self.addr = (self.server, self.port, 0, 0)
        self.id = self.connect()
        print(self.id)

    def connect(self):
      try:
          self.client.connect(self.addr)
          return self.client.recv(2048).decode()
      except:
          pass
 
    def send(self, data):
        try:
           self.client.send(str.encode(data))
           return self.client.recv(2048).decode()
        except socket.error as e:
           print(e)

n = Network()
print(n.send("Hello"))

