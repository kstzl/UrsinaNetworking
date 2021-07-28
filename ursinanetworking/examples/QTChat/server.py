from ursinanetworking import *

Server = UrsinaNetworkingServer("localhost", 25565)

def broadcast_message(message, author):
    Server.broadcast("receive_message", {"message" : message, "author" : author})

@Server.event
def onClientConnected(client):
    client.registered = False
    #broadcast_message(f"{client} connected", "system")

@Server.event
def send_message(client, datas):
    if not client.registered:
        client.registered = True
        client.name = datas
        client.send_message("clear_chat", "")
        client.send_message("get_identity", {"id" : client.id, "name" : client.name})

        broadcast_message(f"{datas} à rejoint le chat !", "système")
    else:
        broadcast_message(datas, client.name)

while True:
    Server.process_net_events()