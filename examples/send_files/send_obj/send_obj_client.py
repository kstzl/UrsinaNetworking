from UrsinaNetworking import UrsinaNetworkingClient
from ursina.mesh_importer import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina import *

app = Ursina()

Client = UrsinaNetworkingClient("localhost", 25565)

class Voxel(Button):
    def __init__(self, position=(0,0,0)):
        super().__init__(
            parent = scene,
            position = position,
            model = "cube",
            origin_y = .5,
            texture = "white_cube",
            color = color.color(0, 0, random.uniform(.9, 1.0)),
            highlight_color = color.lime,
        )

for z in range(8):
    for x in range(8):
        voxel = Voxel(position=(x,0,z))

player = FirstPersonController()

@Client.event
def receiveFile(C):
    f = open("received_model.obj", "wb")
    f.write(C)
    f.close()
    Monkey = Entity(model = "received_model.obj", position = (5, 1, 5), scale = 1)

Client.send_message("requestFile", "Send me the filesss ! ")

app.run()