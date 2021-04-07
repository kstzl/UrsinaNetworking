from UrsinaNetworking import UrsinaNetworkingServer

Server = UrsinaNetworkingServer("localhost", 25565)

@Server.event
def clientDisconnected(Player):
    Server.broadcast("receiveMessage", {"sender" : Player.name, "message" : "Left the chat "})
    print(f"{Player} left the chat !")

@Server.event
def changeName(Player, NewName):
    Server.broadcast("receiveMessage", {"sender" : NewName, "message" : "Joined the chat !"})
    print(f"{NewName} joined the chat !")
    Player.name = NewName

@Server.event
def requestSendMessage(Player, Message):
    Server.broadcast("receiveMessage", {"sender" : Player.name, "message" : Message})