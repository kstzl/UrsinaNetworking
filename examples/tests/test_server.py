from UrsinaNetworking import UrsinaNetworkingServer

Server = UrsinaNetworkingServer("localhost", 25565)

@Server.event
def clientConnected(Client):
    print(f"{Client} connected !")

@Server.event
def clientDisconnected(Client):
    print(f"{Client} disconnected !")

@Server.event
def HelloFromClient(Client, Content):
    print(f"Receveid '{Content}' from {Client}")
    Client.send_message("HelloFromServer", f"Hey {Client} how are you ? :D")
    Server.broadcast("Broadcast", Server.get_clients_ids())