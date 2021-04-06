from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from UrsinaNetworking import UrsinaNetworkingClient
from EasyUrsinaNetworking import EasyUrsinaNetworkingClient, EasyUrsinaNetworkingEntity

Client = UrsinaNetworkingClient("localhost", 8888)
EasyNetworking = EasyUrsinaNetworkingClient(Client)

Entities = {}

window.borderless = False

class Voxel(Button):
    def __init__(self, position=(0,0,0), id = None):
        super().__init__(
            parent = scene,
            position = position,
            model = 'cube',
            origin_y = .5,
            texture = 'white_cube',
            color = color.color(0, 0, random.uniform(.9, 1.0)),
            highlight_color = color.lime,
        )
        self.id = id

    def input(self, key):
        if self.hovered:
            if key == 'right mouse down':
                EasyNetworking.track_entity({ "Type" : "Block", "Pos" : self.position + mouse.normal })
            if key == 'left mouse down':
                EasyNetworking.untrack_entity_by_id(self.id)
                print(f"Trying to remove {self.id} ")
                #Sometimes, destroy is not correctly called ... :/
                #So if the client destroy a "incorrect" cube, so it will automaticaly destroy it!
                if not self.id in EasyNetworking.entities:
                    destroy(self)

@EasyNetworking.event
def entityUpdated(Id, NewDatas):
    Type = NewDatas["Type"]
    if Type == "Player":
        Entities[Id].position = NewDatas["Pos"]
        Entities[Id].rotation = NewDatas["Rot"]

@EasyNetworking.event
def first(myId_):
    global myId
    myId = myId_
    print(f"-------------Hello, i'm {myId}")

@EasyNetworking.event
def entitySpawned(Entity_):
    print(f"ENTITY_SPAWNED : {Entity_}")
    index = Entity_.id
    if Entity_.datas["Type"] == "Player":
        Entities[index] = Entity(collision = False, collider = "", parent = scene, model="cube", texture="white_block", position = (index, 0, 0), scale = (0.5, 1, 0.5))
    elif Entity_.datas["Type"] == "Block":
        Entities[index] = Voxel(position = Entity_.datas["Pos"], id = index)

@EasyNetworking.event
def entityDestroyed(Entity_):
    print(f"Receveid BREAK CALL {Entity_.id}")
    destroy(Entities[Entity_.id])
    print(EasyNetworking.entities)

App = Ursina()
Player = FirstPersonController()

def update():
    if myId:
        ActualData = EasyNetworking.get_entity_data(myId)
        if ActualData != None:
            ActualData["Pos"] = Player.position + Vec3(0, 1, 0)
            ActualData["Rot"] = Player.rotation
            EasyNetworking.update_entity(myId, ActualData)

App.run()