from serverPlayer import *

class serverChat:
    def __init__(self):
        self.chatlog = []

    def addChatLine(player, chatLine):
        if len(chatlog) < 11:
            chatlog.append((player, chatLine))
        else:
            del chatlog[0]
            chatlog.append((player, chatLine))

    def getChatlog(self):
        return self.chatlog









