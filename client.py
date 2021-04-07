from UrsinaNetworking import UrsinaNetworkingClient

Client = UrsinaNetworkingClient("localhost", 25565)

@Client.event
def HelloFromServer(Content):
    print(f"Server says : {Content}")
    
while True:
    Client.process_net_events()