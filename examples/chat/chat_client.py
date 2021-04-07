from UrsinaNetworking import UrsinaNetworkingClient
import threading

Client = UrsinaNetworkingClient("localhost", 25565)

def sendThread():
    while True:
        Client.send_message("requestSendMessage", input("> "))

@Client.event
def connectionEtablished():
    Client.send_message("changeName", input("What's your name ? "))
    threading.Thread(target = sendThread).start()

@Client.event
def receiveMessage(Message):
    SenderName = Message["sender"]
    Content = Message["message"]
    print(f"[{SenderName}] : {Content}")