from ursina import color, raycast
from math import *

from block import *

class Grass(Block):
    def __init__(self, position = (0, 0, 0)):
        super().__init__(position)
        self.texture = "textures/grass_block.png"
        self.sound = "sounds/Grass_dig1.ogg"

class Leave(Block):
    def __init__(self, position = (0, 0, 0)):
        super().__init__(position)
        self.texture = "textures/leave_block.png"
        self.sound = "sounds/Grass_dig1.ogg"

class Wood(Block):
    def __init__(self, position = (0, 0, 0)):
        super().__init__(position)
        self.texture = "textures/wood_block.png"
        self.sound = "sounds/Wood_dig2.ogg"

class Sand(Block):
    def __init__(self, position = (0, 0, 0)):
        super().__init__(position)
        self.texture = "textures/sand_block.png"
        self.sound = "sounds/Sand_dig4.ogg"

class Glass(Block):
    def __init__(self, position = (0, 0, 0)):
        super().__init__(position)
        self.texture = "textures/glass_block.png"
        self.sound = "sounds/Stone_hit3.ogg"
        self.break_sound = "Glass_dig2.ogg"

class Tnt(Block):
    def __init__(self, position = (0, 0, 0)):
        super().__init__(position)
        self.texture = "textures/tnt_block.png"
        self.sound = "sounds/Grass_dig1.ogg"
        self.i = 0
        self.s = 0
        self.breakable = False

    def update(self):
        self.scale = (self.s, self.s, self.s)
        self.s = 0.5 + math.fabs(math.sin(self.i) * 0.05)
        self.i += 0.5