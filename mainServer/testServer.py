import socket
import sys

from clueLServer import *
from cluePServer import *

p1 = Player('12')
l1 = Lobby()


print(p1.getAddress())

l1.addPlayer(p1)

print(l1.returnPNumber())







