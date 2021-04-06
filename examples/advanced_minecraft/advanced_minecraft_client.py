from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from UrsinaNetworking import UrsinaNetworkingClient

Client = UrsinaNetworkingClient("localhost", 8888)
PlayersIds = []
PlayersObject = []

class Voxel(Button):
    def __init__(self, position=(0,0,0)):
        super().__init__(
            parent = scene,
            position = position,
            model = 'cube',
            origin_y = .5,
            texture = 'white_cube',
            color = color.color(0, 0, random.uniform(.9, 1.0)),
            highlight_color = color.lime,
        )

    def input(self, key):
        if self.hovered:
            if key == 'right mouse down':
                Client.send_message("requestSpawnBlock", self.position + mouse.normal)
            if key == 'left mouse down':
                Client.send_message("requestBreakBlock", self.position)
                
class Player(Entity):
    def __init__(self, position=(0,0,0)):
        super().__init__(
            parent = scene,
            position = position,
            model = 'cube',
            texture = 'red_cube',
            origin_y = -0.5,
            scale = (0.1, 1, 0.1),
            color = color.color(0, 0, random.uniform(.9, 1.0)),
            highlight_color = color.lime,
        )

def createPlayer(Id_):
    PlayersObject.append({
        "id" : Id_,
        "ent" : Player(position = (Id_, 0, 0))
    })
    print(f"Created {Id_}")

@Client.event
def getPlayers(PlayersIds_):
    global PlayersIds
    PlayersIds = PlayersIds_

@Client.event
def playerConnected(PlayerId):
    if not PlayerId in PlayersIds:
        PlayersIds.append(PlayerId)
        createPlayer(PlayerId)

@Client.event
def playerDisconnected(PlayerId):
    PlayersIds.remove(PlayerId)
    destroy(PlayersObject[PlayerId]["ent"])
    del PlayersObject[PlayerId]
    print(f"Removed {PlayerId}")

@Client.event
def updatePlayerPosition(Datas):
    try:
        print(Datas)
        PlayerId = Datas["id"]
        NewPosition = Datas["pos"]
        PlayersObject[PlayerId]["ent"].position = NewPosition
    except Exception as e:
        print(e)

@Client.event
def getBlocks(Blocks):
    global BlocksToBuild
    BlocksToBuild = Blocks

@Client.event
def receiveSpawnBlock(Position):
    Voxel(position = Position)

@Client.event
def receiveBreakBlock(Position):
    for block in scene.entities:
        if block.position == Position:
            destroy(block)

#Waiting to get all players
while not len(PlayersIds): pass

App = Ursina()

PointLight(position = (4, 1, 4))

SelfPly = FirstPersonController()

for blockPosition in BlocksToBuild:
    Voxel(position = blockPosition)

for id in PlayersIds:
    createPlayer(id)

def update():
    if SelfPly.y < -1:
        SelfPly.position = (0, 0, 0)
    Client.send_message("requestUpdatePlayerPosition", SelfPly.position)

App.run()

