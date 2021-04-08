from UrsinaNetworking import UrsinaNetworkingServer
from EasyUrsinaNetworking import EasyUrsinaNetworkingServer
import random

Server = UrsinaNetworkingServer("localhost", 25565)
Easy = EasyUrsinaNetworkingServer(Server)

for z in range(5):
    for x in range(5):
        Easy.create_replicated_variable("", {"type" : "block", "position" : (x, 0, z)})

while True:
    Easy.process_net_events()