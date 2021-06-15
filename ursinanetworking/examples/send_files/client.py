from ursinanetworking import *

Client = UrsinaNetworkingClient("localhost", 25565)

@Client.event
def onConnectionEtablished():
    print("I'm connected ! I will request the file to the server ...")
    Client.send_message("requestFile", "")

@Client.event
def receiveFile(Content):
    f = open("receveid_image.png", "wb")
    f.write(ursina_networking_decompress_file(Content))
    f.close()
    print("Thank you !")

while True:
    Client.process_net_events()