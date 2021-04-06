from UrsinaNetworking import UrsinaNetworkingClient
from UrsinaNetworking import ursina_networking_decompress_file

Client = UrsinaNetworkingClient("localhost", 25565)

@Client.event
def ReceiveFile(C):
    print(C)
    f = open("recv.png", "wb")
    f.write(ursina_networking_decompress_file(C))
    f.close()
    print("Done.")