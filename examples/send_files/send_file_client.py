from UrsinaNetworking import UrsinaNetworkingClient

Client = UrsinaNetworkingClient("localhost", 25565)

@Client.event
def ReceiveFile(C):
    print(C)
    f = open("recv.png", "wb")
    f.write(C)
    f.close()
    print("Done.")