from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from UrsinaNetworking import UrsinaNetworkingClient

#Setting up networking

Client = UrsinaNetworkingClient("localhost", 8888)

Players = []
NeedToBuildPlayer = True

@Client.event
def connectionEtablished():
    print("I'm connected ! :D")
    
@Client.event
def getBlocks(Blocks):
    global BlocksToBuild
    BlocksToBuild = Blocks

@Client.event
def connectionError(Error):
    print(f"Oops, {Error}")

@Client.event
def receiveSpawnBlock(Position):
    Voxel(position = Position)

@Client.event
def receiveBreakBlock(Position):
    for block in scene.entities:
        if block.position == Position:
            destroy(block)

App = Ursina()

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

for blockPosition in BlocksToBuild:
    Voxel(position = blockPosition)

player = FirstPersonController()

def update():
    if player.y < -1:
        player.position = (0, 0, 0)

App.run()