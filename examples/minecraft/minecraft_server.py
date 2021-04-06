from UrsinaNetworking import UrsinaNetworkingServer

Server = UrsinaNetworkingServer("localhost", 8888)

Blocks = []

for z in range(8):
    for x in range(8):
        Blocks.append((x,0,z))

@Server.event
def playerConnected(NewPlayer):
    print(f"{NewPlayer} connected ! {Blocks}")
    NewPlayer.send_message("getBlocks", Blocks)

@Server.event
def playerDisconnected(NewPlayer):
    print(f"{NewPlayer} disconnected ! ")

@Server.event
def requestSpawnBlock(Player, Position):
    print(f"{Player} want to spawn a block at {Position} ")
    Blocks.append(Position)
    Server.broadcast("receiveSpawnBlock", Position)

@Server.event
def requestBreakBlock(Player, Position):
    print(f"{Player} want to break a block at {Position} ")
    Blocks.remove(Position)
    Server.broadcast("receiveBreakBlock", Position)
