import socket
import sys

class Player:
    def __init__(self, playerId, conn, addr):
        self.id = playerId
        self.conn = conn
        self.address = addr
        self.ready = False

    def getConn(self):
        return self.conn

    def getAddress(self):
        return self.address

    def setReady(self):
        self.ready = true

    def getReady(self):
        return self.ready

    def connected(self):
        self.conn.send(str.encode(str(self.id) + ".connected"))

