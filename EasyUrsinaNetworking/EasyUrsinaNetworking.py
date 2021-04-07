from UrsinaNetworking import UrsinaNetworkingServer, UrsinaNetworkingClient

class EasyUrsinaNetworkingEvents():

    def __init__(self):
        self.handlers = {}

    def call(self, type, *args):
        if type in self.handlers:
            for h in self.handlers[type]:
                h(*args)

    def event(self, func):
        self.handlers[func.__name__] = [func]

class EasyUrsinaNetworkingEntity:
    def __init__(self, id, datas):
        self.id = id
        self.datas = datas

    def __repr__(self):
        return f"[{self.id} : {self.datas}]"

class EasyUrsinaNetworkingServer:
    def __init__(self, server):
        self.server = server
        self.entities = []
        self.ev = EasyUrsinaNetworkingEvents()
        self.event = self.ev.event

        @self.server.event
        def clientConnected(Ply):
            Ply.send_message("get_all_entities", self.entities)
            self.ev.call("clientConnected", Ply)
            Ply.send_message("first_from_server", len(self.entities) - 1)
            print(f"[EASY NETWORKING] {Ply} connected ! Sending all entities ... ({self.entities})")

        @self.server.event
        def playerDisconnected(Ply):
            print(f"[EASY NETWORKING] {Ply} disconnected ! ")
            self.ev.call("playerDisconnected", Ply)

        @self.server.event
        def request_untrack_entity_by_id(Ply, Id):
            self.untrack_entity_by_id(Id)

        @self.server.event
        def request_track_entity(Ply, EntityData):
            self.track_entity(EntityData)

        @self.server.event
        def request_update(Ply, datas):
            self.update_entity(datas["id"], datas["new_datas"])

    def update_entity(self, id, datas):
        self.entities[id].datas = datas
        self.server.broadcast("datas_updated", {"id" : id, "new_datas" : datas})

    def track_entity(self, EntityData):
        datas = EasyUrsinaNetworkingEntity(len(self.entities), EntityData)
        self.entities.append(datas)
        self.server.broadcast("new_entity_receveid", datas)

    def untrack_entity_by_id(self, EntityId):
        index = 0
        valid = False
        for ent in self.entities:
            if ent.id == EntityId:
                self.server.broadcast("untrack_entity_receveid", { "id" : index, "copy" : ent})
                valid = True
                del self.entities[index]
            index += 1

        if not valid:
            self.server.broadcast("bad_entity", EntityId)
            print(f"[EASY NETWORKING] WARNING : ({EntityId}) is not a valid entity !")
        

class EasyUrsinaNetworkingClient:
    def __init__(self, client):
        self.client = client
        self.entities = []
        self.ev = EasyUrsinaNetworkingEvents()
        self.event = self.ev.event

        @self.client.event
        def get_all_entities(Ents):
            self.entities = Ents
            for e in Ents:
                self.ev.call("entitySpawned", e)

        @self.client.event
        def first_from_server(myId_):
            self.ev.call("first", myId_)

        @self.client.event
        def new_entity_receveid(NewEnt):
            self.entities.append(NewEnt)
            self.ev.call("entitySpawned", NewEnt)

        @self.client.event
        def untrack_entity_receveid(Datas):
            del self.entities[Datas["id"]]
            self.ev.call("entityDestroyed", Datas["copy"])

        @self.client.event
        def datas_updated(Datas):
            self.ev.call("entityUpdated", Datas["id"], Datas["new_datas"])

    def untrack_entity_by_id(self, Id):
        self.client.send_message("request_untrack_entity_by_id", Id)

    def track_entity(self, Entity):
        self.client.send_message("request_track_entity", Entity)

    def get_entity(self, id):
        return self.entities[id]

    def get_entity_data(self, id):
        return self.get_entity(id).datas

    def update_entity(self, id, datas):
        self.client.send_message("request_update", {"id" : id, "new_datas" : datas})