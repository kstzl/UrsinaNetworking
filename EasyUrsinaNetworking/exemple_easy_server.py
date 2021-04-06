from ursina import *
import time, threading
from UrsinaNetworking import UrsinaNetworkingServer
from EasyUrsinaNetworking import EasyUrsinaNetworkingServer

Server = UrsinaNetworkingServer("localhost", 8888)
EasyNetworking = EasyUrsinaNetworkingServer(Server)

print(EasyNetworking.entities)

@EasyNetworking.event
def playerConnected(Ply):
    EasyNetworking.track_entity({ "Type" : "Player", "Id" : Ply.id, "Pos" : Vec3(0, 0, 0), "Rot" : Vec3(0, 0, 0) })

@EasyNetworking.event
def playerDisconnected(Ply):
    for e in EasyNetworking.entities:
        if e.id == Ply.id:
            EasyNetworking.untrack_entity_by_id(e.id)

for x in range(8):
    for y in range(8):
        EasyNetworking.track_entity({ "Type" : "Block", "Pos" : Vec3(x, 0, y) })