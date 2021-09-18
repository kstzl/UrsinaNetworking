from replicated_2 import *
from ursinanetworking import *
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import threading
import time
from shared import *

app = Ursina()
window.borderless = False

Client = UrsinaNetworkingClient("localhost", 25565)
Blabla = ReplicatedClEventsHandler(Client)

PointLight(position = (4, 1, 4))

def update():
    Client.process_net_events()
    Blabla.replicated_update()

player = FirstPersonController()
app.run()