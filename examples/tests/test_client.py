from UrsinaNetworking import UrsinaNetworkingClient

Client = UrsinaNetworkingClient("localhost", 25565)

@Client.event
def connectionEtablished():
    Client.send_message("HelloFromClient", "Hello ! :D")

@Client.event
def HelloFromServer(C):
    print(f"Receveid '{C}' from server !")

@Client.event
def Broadcast(C):
    print(f"BROADCAST {C}")