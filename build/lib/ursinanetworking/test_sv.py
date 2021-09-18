from ursinanetworking import *
from easyursinanetworking import *

Server = UrsinaNetworkingServer("localhost", 25565)
Easy = EasyUrsinaNetworkingServer(Server)

Easy.create_replicated_variable("MyVariable", {"name" : "kevin"})
Easy.update_replicated_variable_by_name("MyVariablee", "name", "jean")
Easy.remove_replicated_variable_by_name("MyVariablee")

while True:
    Easy.process_net_events()