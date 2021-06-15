from ursinanetworking import *

Server = UrsinaNetworkingServer("localhost", 25565)

@Server.event
def requestFile(Client, Content):
    print(f"Ok {Client} ! I will send you the file :D")
    Client.send_message("receiveFile", ursina_networking_encode_file("my_image.png"))

while True:
    Server.process_net_events()