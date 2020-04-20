##
## this function provides the user with a small file defining the connection to the server
##
import socket

## class defines the network connection for the client
class Network:
   def __init__(self):
       self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       self.server = "45.132.241.193"
       self.port   = 42069
       self.addr   = (self.server, self.port)
       self.id     = self.connect()
       print(self.id)

## connects the client to the server and recieves information back
## currently unused but will be important later? or removed later?
   def connect(self):
       try:
           self.client.connect(self.addr)
           return self.client.recv(2048).decode()

       except:
##           print("Epic fail can't even get on the server")
           pass



## sends info to the server and recieves it back 
   def send(self, data):
       try:
           self.client.send(str.encode(data))
           return self.client.recv(2048).decode()

       except socket.error as e:
           print(e)








