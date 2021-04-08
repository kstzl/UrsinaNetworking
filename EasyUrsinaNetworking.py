import UrsinaNetworking
import threading

def easy_ursina_networking_log(Class_, Context_, Message_):

    print(f"[{Class_} / {Context_}] {Message_}")

class EasyUrsinaNetworkingServer():

    def __init__(self, server):
        self.server = server

        @self.server.event
        def onClientConnected(Client):
            print(f"---------------- {Client}")