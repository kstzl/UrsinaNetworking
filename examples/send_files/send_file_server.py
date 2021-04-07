from UrsinaNetworking import UrsinaNetworkingServer, ursina_networking_encode_file

Server = UrsinaNetworkingServer("localhost", 25565)

@Server.event
def clientConnected(Ply):
    Ply.send_message("ReceiveFile", ursina_networking_encode_file("image.png"))