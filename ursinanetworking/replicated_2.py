from ursina import *
import inspect
import uuid
import traceback

from ursinanetworking.ursinanetworking import UrsinaNetworkingClient, UrsinaNetworkingServer

def replicated_generate_id():
    return f"replicated_{str(uuid.uuid4())}"

def replicated_log(str):
    print(f"[REPLICATED] {str}")

def replicated_compact(caller, func, args, kwargs):
    return {
        "id" : caller.id,
        "func_name" : func.__name__,
        "args" : args,
        "kwargs" : kwargs
    }

def replicated_destroy(object):
    object_id = object.id
    object.need_destroy = True
    replicated_log(f"Requested a destroy for object with the id of : {object_id}")


class Replicator():
    def __init__(self) -> None:
        self.id = replicated_generate_id()
        self.class_name = None
        self.handler = None
        self.network_handler = None
        self.need_destroy = False
        self.replicates = []
        self.auto_datas = {}

        replicated_log(f"Object successfully replicated ! (id : {self.id})")

    def set_handler(self, new_handler):
        self.handler = new_handler

        if type(self.handler) == UrsinaNetworkingServer:
            if hasattr(self, "init_server"): self.init_server()
            
        if type(self.handler) == UrsinaNetworkingClient:
            if hasattr(self, "init_client"): self.init_client()

    def replicate(self, arg):
        self.replicates.append(arg)

    def rpc_server(self, func, *args, **kwargs):
        self.handler.send_message("replicated_sv_rpc", replicated_compact(self, func, args, kwargs))

    def rpc_multicast(self, func, *args, **kwargs):
        self.handler.broadcast("replicated_cl_rpc", replicated_compact(self, func, args, kwargs))

class ReplicatedSvEventsHandler:
    def __init__(self, server) -> None:
        self.server = server
        self.replicated_objects = {}
        self.delay = 0.01

        replicated_log(f"Handler initiated ! (delay : {self.delay}s)")

        @self.server.event
        def onClientConnected(client):
            client.send_message("replicated_cl_welcome", self.replicated_objects)

        @self.server.event
        def replicated_sv_rpc(client, datas):
            func = getattr(self.replicated_objects[datas["id"]]["server_instance"], datas["func_name"])
            func(*datas["args"], **datas["kwargs"])

    def create_replicated_object(self, class_name, *args, **kwargs):
        object_instance = class_name(*args, **kwargs)
        object_instance.class_name = class_name
        object_instance.replicated_handler = self
        object_instance.set_handler(self.server)
        added = self.replicated_objects[object_instance.id] = {
            "server_instance" : object_instance,
            "id" : object_instance.id,
            "class_name" : object_instance.class_name,
            "args" : args,
            "kwargs" : kwargs
        }
        self.server.broadcast("replicated_cl_new_object", added)
        return object_instance

    def replicated_update(self):
        r_replicates = []
        r_to_destroy = []

        for i in self.replicated_objects:
            e = self.replicated_objects[i]["server_instance"]

            if hasattr(e, "tick_server"): e.tick_server()

            if e.need_destroy == True:
                self.server.broadcast("replicated_cl_destroy", e.id)
                r_to_destroy.append(e.id)
            else:
                for replicate in e.replicates:
                    r_replicates.append({
                        "id" : e.id,
                        "name" : replicate,
                        "value" : getattr(e, replicate)
                    })
                
                #print(r_replicates)

        self.server.broadcast("replicated_cl_update", r_replicates)

        for i in r_to_destroy:
            destroy(self.replicated_objects[i]["server_instance"])
            del self.replicated_objects[i]
            replicated_log(f"Removed : {i}")

        time.sleep(self.delay)


class ReplicatedClEventsHandler:
    def __init__(self, replicated_context) -> None:
        self.client = replicated_context
        self.replicated_objects = {}
        self.auto_datas = {}
        
        @self.client.event
        def replicated_cl_welcome(datas):
            for e in datas:
                self.add_object_by_network_datas(datas[e])

        @self.client.event
        def replicated_cl_new_object(object_data):
            self.add_object_by_network_datas(object_data)

        @self.client.event
        def replicated_cl_update(datas):
            for e in datas:
                setattr(self.replicated_objects[e["id"]], e["name"], e["value"])

        @self.client.event
        def replicated_cl_rpc(datas):
            func = getattr(self.replicated_objects[datas["id"]], datas["func_name"])
            func(*datas["args"], **datas["kwargs"])

        @self.client.event
        def replicated_cl_destroy(object_id):
            object_to_delete = self.replicated_objects[object_id]
            destroy(object_to_delete)
            del self.replicated_objects[object_id]
            replicated_log(f"Removed : {object_id}")

    def add_object_by_network_datas(self, object_data):
        id = object_data["id"]
        object_instance = object_data["class_name"](*object_data["args"], **object_data["kwargs"])
        object_instance.set_handler(self.client)
        object_instance.replicated_handler = self
        object_instance.id = id
        object_instance.auto_datas = self.auto_datas
        self.replicated_objects[id] = object_instance

    def replicated_update(self):
        for e in self.replicated_objects:
            if hasattr(self.replicated_objects[e], "tick_client"):
                self.replicated_objects[e].tick_client()