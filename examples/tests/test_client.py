from UrsinaNetworking import UrsinaNetworkingClient

Client = UrsinaNetworkingClient("localhost", 25565)

@Client.event
def connectionEtablished():
    Client.send_message("HelloFromClient", "Hello ! :D")

@Client.event
def HelloFromServer(Content):
    print(f"Receveid '{Content}' from server !")

@Client.event
def Broadcast(Content):
    print(f"BROADCAST RECEVEID ! {Content}")