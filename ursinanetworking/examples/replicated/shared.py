from ursina import *
from ursinanetworking import *

class TestObject(Button, Replicator):
    def __init__(self, position=(-1,1,0)):

        Button.__init__(
            self,
            parent = scene,
            position = position,
            model = 'cube',
            origin_y = .5,
            texture = 'stone_tex.bmp',
            color = color.color(0, 0, random.uniform(.9, 1.0)),
            highlight_color = color.lime,
        )

        self.sfx = Audio("stone_dig.ogg", autoplay=False)
        Replicator.__init__(self)
        #self.replicate("position")

    def destroy_server(self):
        replicated_destroy(self)
        self.rpc_multicast(self.sfx_multicast, 0.5)

    def place_server(self, pos):
        a = self.replicated_handler.create_replicated_object(TestObject, position = pos)
        self.rpc_multicast(self.sfx_multicast, 1)

    def sfx_multicast(self, pitch):
        self.sfx.pitch = pitch
        self.sfx.play()

    def input(self, key):
        if self.hovered and key == "left mouse down":
            self.rpc_server(self.destroy_server)
        if self.hovered and key == "right mouse down":
            self.rpc_server(self.place_server, self.position + mouse.normal)