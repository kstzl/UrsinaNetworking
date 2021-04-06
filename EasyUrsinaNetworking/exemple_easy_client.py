from ursina import *
from UrsinaNetworking import UrsinaNetworkingClient
from EasyUrsinaNetworking import EasyUrsinaNetworkingClient, EasyUrsinaNetworkingEntity

Client = UrsinaNetworkingClient("localhost", 8888)
EasyNetworking = EasyUrsinaNetworkingClient(Client)

Entities = {}

window.borderless = False

@EasyNetworking.event
def entityUpdated(Id, NewDatas):
    Type = NewDatas["Type"]
    if Type == "Player":
        Entities[Id].position = NewDatas["Pos"]

@EasyNetworking.event
def first(myId_):
    global myId
    myId = myId_
    print(f"-------------Hello, i'm {myId}")

@EasyNetworking.event
def entitySpawned(Entity_):
    index = Entity_.id
    if Entity_.datas["Type"] == "Player":
        Entities[index] = Button(parent = scene, model="cube", texture="white_block", position = (index, 0, 0))

@EasyNetworking.event
def entityDestroyed(Entity_):
    print(f"Destroyed {Entity}")
    Entities[Entity_.id].scale = (0.5, 0.5, 0.5)
    destroy(Entities[Entity_.id])
    del Entities[Entity_.id]

App = Ursina()

def update():
    Speed = 10 * time.dt
    ActualData = EasyNetworking.get_entity_data(myId)
    NewPos = ActualData["Pos"] + Vec3(held_keys["d"] * Speed - held_keys["a"] * Speed, held_keys["w"] * Speed - held_keys["s"] * Speed, 0)
    ActualData["Pos"] = NewPos
    EasyNetworking.update_entity(myId, ActualData)

App.run()