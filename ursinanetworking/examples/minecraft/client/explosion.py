from ursina import *
from ursina.curve import *

class Explosion(Entity):
    def __init__(self, position) -> None:
        super().__init__(
            model = "quad",
            texture = "textures/explosion",
            origin_y = -0.25,
            scale = (0, 0, 0),
            billboard = True,
            position = position
        )
        self.ad = Audio("sounds/tnt.mp3")
        self.ad.volume = 2
        self.ad.play()

        self.animate_scale((3, 3, 3), 1)
        self.animate_color(color.rgba(0, 0, 0, 0), 1)

        destroy(self, 1)