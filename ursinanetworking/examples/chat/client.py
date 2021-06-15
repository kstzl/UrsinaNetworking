from ursinanetworking import *
import threading

Client = UrsinaNetworkingClient("localhost", 25565)

MessagesToSend = []

def sendMessageThread():
    while True:
        MessagesToSend.append(input(">"))

@Client.event
def onConnectionEtablished():
    Client.send_message("changeName", input("What's your name ? "))
    threading.Thread(target = sendMessageThread).start()

@Client.event
def messageReceveid(message):
    print(message)

while True:

    #This for avoiding races conditions due to threads
    for message in MessagesToSend:
        Client.send_message("message", message)
    MessagesToSend.clear()

    Client.process_net_events()