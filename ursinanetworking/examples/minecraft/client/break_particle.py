from ursina import *
from ursina.shaders import basic_lighting_shader
from random import *

class BreakParticle(Entity):

    def __init__(self, texture, position = (0,0,0)):
        super().__init__(
            position = position,
            model = "block",
            texture = texture,
            origin_y = .5,
            billboard = True,
            color = color.white,
            highlight_color = color.white,
            scale = (
                uniform(0.01, 0.25),
                uniform(0.01, 0.25),
                uniform(0.0, 0.0)
            ),
            shader = basic_lighting_shader
        )

        self.s = 0.05
        self.velx = uniform(-self.s, self.s)
        self.vely = uniform(0, 0.1)
        self.velz = uniform(-self.s, self.s)
        self.animate_scale(0, uniform(0.75, 1))
        destroy(self, 1)
    
    def update(self):
        r = raycast(self.position , (0, -1, 0), ignore=(self,), distance=0.1, debug=False).hit
        if not r:
            self.position += (self.velx, self.vely, self.velz)
            self.vely -= 0.009