from replicated_2 import *
from ursinanetworking import *
import threading
from shared import *

Server = UrsinaNetworkingServer("localhost", 25565)
Blabla = ReplicatedSvEventsHandler(Server)

for z in range(8):
    for x in range(8):
        new_block = Blabla.create_replicated_object(TestObject, position = (x, 0, z))

while True:
    Server.process_net_events()
    Blabla.replicated_update()