from UrsinaNetworking import UrsinaNetworkingServer, ursina_networking_encode_file

Server = UrsinaNetworkingServer("localhost", 25565)

@Server.event
def requestFile(Ply, Datas):
    print("Ok, no problem ! Sending file ...")
    Ply.send_message("receiveFile", ursina_networking_encode_file("cone.obj"))

@Server.event
def playerDisconnected(Ply):
    print(f"{Ply} disconnected ")