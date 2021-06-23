from ursina import *
from ursina.shaders import basic_lighting_shader
from ursinanetworking import *

BLOCKS_PARENT = Entity()

class Block(Button):

    def __init__(self, position = (0,0,0)):
        super().__init__(
            parent = BLOCKS_PARENT,
            position = position,
            model = "block",
            origin_y = .5,
            color = color.white,
            highlight_color = color.white,
            scale = .5,
            shader = basic_lighting_shader
        )
        self.name = "unnamed_block"
        self.sound = None
        self.break_sound = None
        self.client = None
        self.breakable = True