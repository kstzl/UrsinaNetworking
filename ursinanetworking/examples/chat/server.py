from UrsinaNetworking import UrsinaNetworkingServer

Server = UrsinaNetworkingServer("localhost", 25565)

@Server.event
def changeName(client, new_name):
    client.name = new_name
    Server.broadcast("messageReceveid", f"{client.name} joined the chat !")

@Server.event
def onClientDisconnected(client):
    Server.broadcast("messageReceveid", f"{client.name} left the chat !")

@Server.event
def message(client, message):
    Server.broadcast("messageReceveid", f"{client.name} : {message}")

while True:
    Server.process_net_events()