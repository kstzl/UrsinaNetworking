from asyncio.tasks import sleep
from random import uniform
from time import *
from ursinanetworking import *
from perlin_noise import PerlinNoise
from opensimplex import OpenSimplex
from ursina import Vec3, distance
import asyncio

print("Hello from the server !")

Server = UrsinaNetworkingServer("localhost", 25565)
Easy = EasyUrsinaNetworkingServer(Server)
Blocks = {}

def Explosion(position):
    Server.broadcast("Explode", position)
    sleep(1)
    to_destroy = []
    for x in Blocks:
        a = (Blocks[x]["position"])
        b = (position)
        if distance(Vec3(a), Vec3(b)) < 2:
            to_destroy.append(x)
    for x in to_destroy:
        destroy_block(x)


# Destroy Block Function
def destroy_block(Block_name):
    del Blocks[Block_name]
    Easy.remove_replicated_variable_by_name(Block_name)

# Spawn Block Function
i = 0
def spawn_block(block_type, position, investigator = "client"):
    global i
    block_name = f"blocks_{i}"
    Easy.create_replicated_variable(
        block_name,
        { "type" : "block", "block_type" : block_type, "position" : position, "investigator" : investigator}
    )
    
    if block_type == "tnt":
        threading.Thread(target = Explosion, args=(position,)).start()

    Blocks[block_name] = {
        "name" : block_name,
        "position" : position
    }
    i += 1

# A little Hello
@Server.event
def onClientConnected(Client):
    Easy.create_replicated_variable(
        f"player_{Client.id}",
        { "type" : "player", "id" : Client.id, "position" : (0, 0, 0) }
    )
    print(f"{Client} connected !")
    Client.send_message("GetId", Client.id)

# A little goodbye
@Server.event
def onClientDisconnected(Client):
    Easy.remove_replicated_variable_by_name(f"player_{Client.id}")

# When a client destroy a block
@Server.event
def request_destroy_block(Client, Block_name):
    destroy_block(Block_name)

# When a client place a block
@Server.event
def request_place_block(Client, Content):
    spawn_block(Content["block_type"], Content["position"])

# Update Player's position
@Server.event
def MyPosition(Client, NewPos):
    Easy.update_replicated_variable_by_name(f"player_{Client.id}", "position", NewPos)

tmp = OpenSimplex()
# Create the world
for x in range(32):
    for z in range(32):

        l = round(tmp.noise2d(x = x / 5, y = z / 5))

        if l == -1: spawn_block("sand", (x, l, z), investigator = "server")
        if l == 0: spawn_block("grass", (x, l, z), investigator = "server")
        if l == 1: spawn_block("leave", (x, l, z), investigator = "server")

while True:
    Easy.process_net_events()