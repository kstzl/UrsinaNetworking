from ursinanetworking import *

from ursina.prefabs.first_person_controller import FirstPersonController
from ursina import *

Client = UrsinaNetworkingClient("localhost", 25565)
Easy = EasyUrsinaNetworkingClient(Client)

class Voxel(Button):
    def __init__(self, position, name):
        super().__init__(
            parent = scene,
            position = position,
            model = "cube",
            texture = "white_cube",
            origin_y = 0.5,
            color = color.color(0,0,random.uniform(0.9,1)),
        )
        self.name = name

    def input(self, key):
        if self.hovered:
            if key == "right mouse down":
                Easy.create_replicated_variable("", {"type" : "block", "position" : self.position + mouse.normal})
            if key == "left mouse down":
                Easy.remove_replicated_variable_by_name(self.name)

@Easy.event
def onReplicatedVariableCreated(variable):
    print(variable)
    if variable.content["type"] == "block":
        Voxel(variable.content["position"], variable.name)

@Easy.event
def onReplicatedVariableRemoved(variable):
    for e in scene.entities:
        if e.position == variable.content["position"]:
            print(f"Calling destroy for {e}")
            destroy(e)

App = Ursina()

Player = FirstPersonController()

def update():
    Easy.process_net_events()

App.run()