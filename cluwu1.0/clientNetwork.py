##
## this function provides the user with a small file defining the connection to the server
##
import socket
import pickle
from clientLobby import *
from clientPlayer import *
from serverCard import *

## class defines the network conenciton for the client
class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "45.132.241.193"
        # self.server = "localhost"
        self.port   = 42069
        # self.port   = 9001
        self.addr   = (self.server, self.port)
        self.id     = self.connect()

## connects the client to the server and recieves information back
## this sets the playid for the client
    def connect(self):
        try:
            self.client.connect(self.addr)
            data = pickle.loads(self.client.recv(2048))
            print("Recieved  --  " + str(data))
            stuff = data.split(":")
            return stuff[0]

        except:
            pass

## this is the command that the client would use sent info the server and get it back
    def send(self, data):
        send = str(self.id)
        send += ":"
        send += data
        try:
            print("    Sent  --  " + send)
            self.client.send(pickle.dumps(send))#encode the objects to binary code which traveling between server and newtork
        except socket.error as e:
            print(e)

## this returns the client their assigned id
    def getId(self):
        return self.id
    
## this catches the objects list 
    def catch(self):
         data = pickle.loads(self.client.recv(4096))
         return data

