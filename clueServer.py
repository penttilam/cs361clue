import socket
from _thread import *
import sys

## this is a IPV4 connection
server = "45.132.241.193"
port = 42069

## this sets up the IPV4 socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

## this actively binds the server to a port
try:
    s.bind((server, port))
except socket.error as e:
    str(e)

## this allows the server to accept a connection limited to: 6
s.listen(6)
print("Clue server started, waiting for players to connect :D")


## the connection to the client 
def threaded_client(conn, player):
   varify = 'Player '+ repr(player) +' Connected'
   conn.send(str.encode(str(varify)))
   reply = ""

   while True:
       try:
           data = conn.recv(2048)
           reply = data.decode("utf-8")

           if not data:
               print("Player ", player, " disconnected")
               break
           else:
               print("Received: ", reply)
               print("Sending : ", reply)

           conn.sendall(str.endcode(reply))

       except:
          break

   print("Lost connection to player ", player)
   conn.close()

## this is the server running 
currentPlayer = 1
while True:
    conn, addr = s.accept()
    print("Connected to: ", addr, " as player ", currentPlayer)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1




