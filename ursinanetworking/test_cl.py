from ursinanetworking import *
from easyursinanetworking import *

Client = UrsinaNetworkingClient("localhost", 25565)
Easy = EasyUrsinaNetworkingClient(Client)

@Easy.event
def onReplicatedVariableCreated(variable):
    print("Variable Created : ")
    print(variable)

@Easy.event
def onReplicatedVariableUpdated(variable):
    print("Variable Updated : ")
    print(variable)

@Easy.event
def onReplicatedVariableRemoved(variable):
    print("Variable Removed : ")
    print(variable)

while True:
    Easy.process_net_events()