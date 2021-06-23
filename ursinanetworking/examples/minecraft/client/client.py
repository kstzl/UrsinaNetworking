from re import A
import threading

from ursina import *
from random import *
from ursina.prefabs.first_person_controller import FirstPersonController
from perlin_noise import PerlinNoise
from ursinanetworking import *
from time import sleep

from blocks import *
from player import *
from player import *
from break_particle import *
from explosion import *

BLOCKS = [
    "grass",
    "leave",
    "wood",
    "sand",
    "glass",
    "tnt"
]

App = Ursina()
Client = UrsinaNetworkingClient("localhost", 25565)
Easy = EasyUrsinaNetworkingClient(Client)
window.borderless = False

Ad = Audio("")
sky = Sky()

Blocks = {}
Players = {}
PlayersTargetPos = {}

SelfId = -1

@Client.event
def Explode(Position):
    E = Explosion(Position)

@Client.event
def GetId(Id):
    global SelfId
    SelfId = Id
    print(f"My ID is : {SelfId}")

@Easy.event
def onReplicatedVariableCreated(variable):
    global Client
    variable_name = variable.name
    variable_type = variable.content["type"]
    if variable_type == "block":
        block_type = variable.content["block_type"]
        if block_type == "grass": new_block = Grass()
        elif block_type == "leave": new_block = Leave()
        elif block_type == "wood": new_block = Wood()
        elif block_type == "sand": new_block = Sand()
        elif block_type == "glass": new_block = Glass()
        elif block_type == "tnt": new_block = Tnt()
        else:
            print("Block not found.")
            return

        new_block.name = variable_name
        new_block.position = variable.content["position"]
        new_block.client = Client
        Blocks[variable_name] = new_block
        if variable.content["investigator"] == "client":
            Ad.clip = new_block.sound
            Ad.pitch = uniform(0.8, 1.2)
            Ad.play()
    elif variable_type == "player":
        PlayersTargetPos[variable_name] = Vec3(0, 0, 0)
        Players[variable_name] = PlayerRepresentation()
        if SelfId == int(variable.content["id"]):
            Players[variable_name].color = color.red
            Players[variable_name].visible = False

@Easy.event
def onReplicatedVariableUpdated(variable):
    PlayersTargetPos[variable.name] = variable.content["position"]

@Easy.event
def onReplicatedVariableRemoved(variable):
    variable_name = variable.name
    variable_type = variable.content["type"]
    if variable_type == "block":
        Ad.clip = Blocks[variable_name].break_sound if Blocks[variable_name].break_sound != None else Blocks[variable_name].sound
        Ad.pitch = uniform(0.5, 0.9)
        Ad.play()

        for i in range(randrange(2, 4)):
            BreakParticle(Blocks[variable_name].texture, Blocks[variable_name].position)

        destroy(Blocks[variable_name])
        del Blocks[variable_name]
    elif variable_type == "player":
        destroy(Players[variable_name])
        del Players[variable_name]

Ply = Player()

MAX = len(BLOCKS)
INDEX = 1
SELECTED_BLOCK = ""

Inventory = Text(text = "", origin = (-5, 0), background = False)

def updateHud():

    Ad.clip = "sounds/gui_click_2.ogg"
    Ad.play()

    global SELECTED_BLOCK
    SELECTED_BLOCK = BLOCKS[INDEX % MAX]
    txt = "Inventory : \n"
    for b in BLOCKS:
        if b == SELECTED_BLOCK:
            txt += f"---> {b}\n"
        else:
            txt += f"{b}\n"
    Inventory.text = txt

updateHud()

def input(key):

    global INDEX, SELECTED_BLOCK

    if key == "right mouse down":
        A = raycast(Ply.position + (0, 2, 0), camera.forward, distance = 6, traverse_target = scene)
        E = A.entity
        if E:
            pos = E.position + mouse.normal
            Client.send_message("request_place_block", { "block_type" : SELECTED_BLOCK, "position" : tuple(pos)})

    if key == "left mouse down":
        A = raycast(Ply.position + (0, 2, 0), camera.forward, distance = 6, traverse_target = scene)
        E = A.entity
        if E and E.breakable:
            Client.send_message("request_destroy_block", E.name)

    if key == "scroll up":
        INDEX -= 1
        updateHud()

    elif key == "scroll down":
        INDEX += 1
        updateHud()

    Client.send_message("MyPosition", tuple(Ply.position + (0, 1, 0)))

def update():

    if Ply.position[1] < -5:
        Ply.position = (randrange(0, 15), 10, randrange(0, 15))

    for p in Players:
        try:
            Players[p].position += (Vec3(PlayersTargetPos[p]) - Players[p].position) / 25
        except Exception as e: print(e)
    
    Easy.process_net_events()

App.run()