from UrsinaNetworking import UrsinaNetworkingServer

Server = UrsinaNetworkingServer("localhost", 8888)

Blocks = []

for z in range(8):
    for x in range(8):
        Blocks.append((x,0,z))

@Server.event
def playerConnected(NewPlayer):
    NewPlayer.send_message("getPlayers", Server.get_clients_ids())
    NewPlayer.send_message("getBlocks", Blocks)
    Server.broadcast("playerConnected", NewPlayer.id)

#Player's position:
@Server.event
def playerDisconnected(NewPlayer):
    Server.broadcast("playerDisconnected", NewPlayer.id)

@Server.event
def requestUpdatePlayerPosition(Player, NewPosition):
    Server.broadcast("updatePlayerPosition", {"id" : Player.id, "pos" : NewPosition})

#Blocks handling
@Server.event
def requestSpawnBlock(Player, Position):
    print(f"{Player} want to destroy a block at {Position} ")
    Blocks.append(Position)
    Server.broadcast("receiveSpawnBlock", Position)

@Server.event
def requestBreakBlock(Player, Position):
    print(f"{Player} want to spawn a block at {Position} ")
    if Position != (0, 0, 0):
        Blocks.remove(Position)
        Server.broadcast("receiveBreakBlock", Position)
    else:
        print("Cant break block at (0, 0, 0)")