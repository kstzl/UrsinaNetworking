"""
  ______                _    _          _             _   _      _                      _    _
 |  ____|              | |  | |        (_)           | \ | |    | |                    | |  (_)
 | |__   __ _ ___ _   _| |  | |_ __ ___ _ _ __   __ _|  \| | ___| |___      _____  _ __| | ___ _ __   __ _
 |  __| / _` / __| | | | |  | | '__/ __| | '_ \ / _` | . ` |/ _ \ __\ \ /\ / / _ \| '__| |/ / | '_ \ / _` |
 | |___| (_| \__ \ |_| | |__| | |  \__ \ | | | | (_| | |\  |  __/ |_ \ V  V / (_) | |  |   <| | | | | (_| |
 |______\__,_|___/\__, |\____/|_|  |___/_|_| |_|\__,_|_| \_|\___|\__| \_/\_/ \___/|_|  |_|\_\_|_| |_|\__, |
                   __/ |                                                                              __/ |
                  |___/                                                                              |___/
By K3#4869

Version 1.0.1
"""

BUILTIN_EVENT_ON_REPLICATED_VARIABLE_CREATED = "onReplicatedVariableCreated"
BUILTIN_EVENT_ON_REPLICATED_VARIABLE_UPDATED = "onReplicatedVariableUpdated"
BUILTIN_EVENT_ON_REPLICATED_VARIABLE_REMOVED = "onReplicatedVariableRemoved"

def easy_ursina_networking_log(Class_, Context_, Message_):

    print(f"[{Class_} / {Context_}] {Message_}")

class EasyUrsinaNetworkingEvents():

    def __init__(self):
        self.events = []
        self.event_table = {}

    def process_net_events(self):
        for event in self.events:
            Func = event[0]
            Args = event[1]
            try:
                for events_ in self.event_table:
                    for event_ in self.event_table[ events_ ]:
                        if Func in event_.__name__:
                            event_(*Args)
            except Exception as e:
                easy_ursina_networking_log("EasyUrsinaNetworkingEvents", "process_net_events", e)
        self.events.clear()

    def event(self, func):
        if func.__name__ in self.event_table:
            self.event_table[func.__name__].append(func)
        else:
            self.event_table[func.__name__]= [func]

class EasyUrsinaNetworkingReplicatedVariable():

    def __init__(self, name, content):
        self.name = name
        self.content = content

    def __repr__(self):
        return f"[Replicated Variable '{self.name}' : '{self.content}']"

class EasyUrsinaNetworkingServer():

    def __init__(self, server):
        self.server = server
        self.replicated_variables = {}
        self.events_manager = EasyUrsinaNetworkingEvents()
        self.event = self.events_manager.event

        @self.server.event
        def onClientConnected(client):
            easy_ursina_networking_log("EasyUrsinaNetworkingServer", "onClientConnected", f"Sending {len(self.replicated_variables)} replicated variable(s) to {client} ...")
            client.send_message("BUILTIN_EVENT_SEND_REPLICATED_VARIABLES", self.replicated_variables)

        @self.server.event
        def BUILTIN_EVENT_REQUEST_CREATE_REPLICATED_VARIABLE(client, variable):
            self.create_replicated_variable(variable.name, variable.content)
            self.events_manager.events.append((BUILTIN_EVENT_ON_REPLICATED_VARIABLE_CREATED, variable))

        @self.server.event
        def BUILTIN_EVENT_REQUEST_REMOVE_REPLICATED_VARIABLE_BY_NAME(client, name):
            if name in self.replicated_variables:
                self.events_manager.events.append((BUILTIN_EVENT_ON_REPLICATED_VARIABLE_REMOVED, self.replicated_variables[name] ))
                self.remove_replicated_variable_by_name(name)

        @self.server.event
        def BUILTIN_EVENT_REQUEST_UPDATE_REPLICATED_VARIABLE_BY_NAME(client, datas):
            self.update_replicated_variable_by_name(datas[0], datas[1])
            self.events_manager.events.append((BUILTIN_EVENT_ON_REPLICATED_VARIABLE_UPDATED, datas[1]))

    def get_replicated_variable_by_name(self, name):
        return self.replicated_variables[name]

    def get_replicated_variables(self):
        return self.replicated_variables

    def create_replicated_variable(self, name, content):
        if name == "": name = f"unnamed_replicated_variable_{len(self.replicated_variables)}"
        self.replicated_variables[name] = (EasyUrsinaNetworkingReplicatedVariable(name, content))
        self.server.broadcast("BUILTIN_EVENT_SEND_CREATE_REPLICATED_VARIABLE", self.replicated_variables[name])

    def remove_replicated_variable_by_name(self, name):
        if not name in self.replicated_variables:
            easy_ursina_networking_log("EasyUrsinaNetworkingServer", "remove_replicated_variable_by_name", f"ERROR ! '{name}' does not exist !")
            return
        try:
            copy = self.replicated_variables[name]
            self.replicated_variables.pop(name, None)
            self.server.broadcast("BUILTIN_EVENT_SEND_REMOVE_REPLICATED_VARIABLE", copy)
        except Exception as e: easy_ursina_networking_log("EasyUrsinaNetworkingServer", "remove_replicated_variable_by_name", f"ERROR : {e}")

    def update_replicated_variable_by_name(self, variable_name, key, content):
        if not variable_name in self.replicated_variables:
            easy_ursina_networking_log("EasyUrsinaNetworkingServer", "update_replicated_variable_by_name", f"ERROR ! '{variable_name}' does not exist !")
            return
        try:
            self.replicated_variables[variable_name].content[key] = content
            self.server.broadcast("BUILTIN_EVENT_SEND_UPDATE_REPLICATED_VARIABLE", self.replicated_variables[variable_name])
        except Exception as e: easy_ursina_networking_log("EasyUrsinaNetworkingServer", "update_replicated_variable_by_name", f"ERROR : {e}")

    def process_net_events(self):
        self.server.process_net_events()
        self.events_manager.process_net_events()

class EasyUrsinaNetworkingClient():

    def __init__(self, client):
        self.client = client
        self.replicated_variables = {}
        self.events_manager = EasyUrsinaNetworkingEvents()
        self.event = self.events_manager.event

        @self.client.event
        def BUILTIN_EVENT_SEND_REPLICATED_VARIABLES(replicated_variables):
            self.replicated_variables = replicated_variables
            for replicated_variable in self.replicated_variables:
                variable_to_send = [self.replicated_variables[replicated_variable]]
                self.events_manager.events.append((BUILTIN_EVENT_ON_REPLICATED_VARIABLE_CREATED, variable_to_send))

        @self.client.event
        def BUILTIN_EVENT_SEND_CREATE_REPLICATED_VARIABLE(replicated_variable):
            self.replicated_variables[replicated_variable.name] = replicated_variable
            self.events_manager.events.append((BUILTIN_EVENT_ON_REPLICATED_VARIABLE_CREATED, [replicated_variable]))

        @self.client.event
        def BUILTIN_EVENT_SEND_REMOVE_REPLICATED_VARIABLE(replicated_variable):
            self.replicated_variables.pop(replicated_variable.name, None)
            self.events_manager.events.append((BUILTIN_EVENT_ON_REPLICATED_VARIABLE_REMOVED, [replicated_variable]))

        @self.client.event
        def BUILTIN_EVENT_SEND_UPDATE_REPLICATED_VARIABLE(updated_variable):
            self.replicated_variables[updated_variable.name].content = updated_variable.content
            self.events_manager.events.append((BUILTIN_EVENT_ON_REPLICATED_VARIABLE_UPDATED, [self.replicated_variables[updated_variable.name]]))

    def process_net_events(self):
        self.client.process_net_events()
        self.events_manager.process_net_events()