from UrsinaNetworking import UrsinaNetworkingServer

Server = UrsinaNetworkingServer("localhost", 25565)

@Server.event
def onClientConnected(Client):
    Client.send_message("HelloFromServer", f"Hello {Client} how are you ?! :D")

while True:
    Server.process_net_events()