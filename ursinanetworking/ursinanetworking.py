"""
  _    _          _             _   _      _                      _    _
 | |  | |        (_)           | \ | |    | |                    | |  (_)
 | |  | |_ __ ___ _ _ __   __ _|  \| | ___| |___      _____  _ __| | ___ _ __   __ _
 | |  | | '__/ __| | '_ \ / _` | . ` |/ _ \ __\ \ /\ / / _ \| '__| |/ / | '_ \ / _` |
 | |__| | |  \__ \ | | | | (_| | |\  |  __/ |_ \ V  V / (_) | |  |   <| | | | | (_| |
  \____/|_|  |___/_|_| |_|\__,_|_| \_|\___|\__| \_/\_/ \___/|_|  |_|\_\_|_| |_|\__, |
                                                                                __/ |
                                                                               |___/
By K3#4869 and Squiggle#1385
"""

import socket
import threading
import pickle
import zlib

HEADERSIZE = 10
MESSAGE_LENGTH = 8
BUFFERSIZE = 4096

BUILTIN_EVENT_CONNECTION_ESTABLISHED = "onConnectionEstablished"
BUILTIN_EVENT_CONNECTION_ERROR      = "onConnectionError"

BUILTIN_EVENT_CLIENT_CONNECTED      = "onClientConnected"
BUILTIN_EVENT_CLIENT_DISCONNECTED   = "onClientDisconnected"

STATE_HEADER    = "STATE_HEADER"
STATE_PAYLOAD   = "STATE_PAYLOAD"

def ursina_networking_log(Class_, Context_, Message_):

    print(f"[{Class_} / {Context_}] {Message_}")

def ursina_networking_decompress_file(Datas_):

    return zlib.decompress(Datas_)

def ursina_networking_encode_file(Path_):

    file = open(Path_, "rb")
    datas = file.read()
    file.close()
    return zlib.compress(datas)

def ursina_networking_encode_message(Message_, Content_):

    try:
        Message = {
            "Message"   :   Message_,
            "Content"   :   Content_
        }
        EncodedMessage = pickle.dumps(Message)
        MessageLength = len(EncodedMessage)
        LengthToBytes = MessageLength.to_bytes(MESSAGE_LENGTH, byteorder = "big")
        FinalMessage = LengthToBytes + EncodedMessage
        return FinalMessage
    except Exception as e:
        ursina_networking_log("ursina_networking_encode_message", "func", e)
    return b""

class UrsinaNetworkingEvents():

    def __init__(self, lock):
        self.events = []
        self.event_table = {}
        self.lock = lock

    def push_event(self, name, *args):
        self.lock.acquire()
        self.events.append((name, args))
        self.lock.release()

    def process_net_events(self):
        self.lock.acquire()
        for event in self.events:
            Func = event[0]
            Args = event[1]
            try:
                for events_ in self.event_table:
                    for event_ in self.event_table[ events_ ]:
                        if Func in event_.__name__:
                            event_(*Args)
            except Exception as e:
                ursina_networking_log("UrsinaNetworkingEvents", "process_net_events", f"Unable to correctly call '{Func}' : '{e}'")
        self.events.clear()
        self.lock.release()

    def event(self, func):
        if func.__name__ in self.event_table:
            self.event_table[func.__name__].append(func)
        else:
            self.event_table[func.__name__]= [func]

class UrsinaNetworinkDatagramsBuffer():

    def __init__(self):
        self.header = bytes()
        self.payload = bytes()
        self.buf = bytearray()
        self.pickled_datas = None
        self.payload_length = 0
        self.receive_all = False
        self.datagrams = []
        self.state = STATE_HEADER

    def receive_datagrams(self, client_):

        self.buf += client_.recv(BUFFERSIZE)

        while True:

            self.state_changed = False

            if self.state == STATE_HEADER:

                if len(self.buf) >= MESSAGE_LENGTH:

                    self.header = self.buf[:MESSAGE_LENGTH]

                    del self.buf[:MESSAGE_LENGTH]

                    self.payload_length = int.from_bytes(self.header, byteorder = "big", signed = False)

                    self.state = STATE_PAYLOAD
                    self.state_changed = True

            elif self.state == STATE_PAYLOAD:

                if len(self.buf) >= self.payload_length:

                    self.payload = self.buf[:self.payload_length]

                    del self.buf[:self.payload_length]

                    self.state = STATE_HEADER
                    self.state_changed = True
                    self.receive_all = True
                    self.pickled_datas = pickle.loads(self.payload)
                    self.datagrams.append(self.pickled_datas)

            if not self.state_changed:
                break

    def receive(self):
        if self.receive_all:
            self.receive_all = False
            return True
        else:
            return False

class UrsinaNetworkingConnectedClient():

    def __init__(self, socket, address, id):
        self.socket = socket
        self.address = address
        self.id = id
        self.name = f"Client {id}"
        self.datas = {}

    def __repr__(self):
        return self.name

    def send_message(self, Message_, Content_):
        try:
            if (Encoded:=ursina_networking_encode_message(Message_, Content_))==b"": return False
            self.socket.sendall(Encoded)
            return True
        except Exception as e:
            ursina_networking_log("UrsinaNetworkingConnectedClient", "send_message", e)
            return False

class UrsinaNetworkingServer():

    def __init__(self, Ip_, Port_):

        self.lock = threading.Lock()
        self.events_manager = UrsinaNetworkingEvents(self.lock)
        self.network_buffer = UrsinaNetworinkDatagramsBuffer()
        self.event = self.events_manager.event
        self.clients = []
        self.lock = threading.Lock()

        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind((Ip_, Port_))
            self.server.listen()
            self.receiveThread = threading.Thread(target = self.receive)
            self.receiveThread.start()

            ursina_networking_log("UrsinaNetworkingServer", "__init__", "Server started !")
            ursina_networking_log("UrsinaNetworkingServer", "__init__", f"Ip   :   {Ip_}")
            ursina_networking_log("UrsinaNetworkingServer", "__init__", f"Port :   {Port_}")

        except Exception as e:
            ursina_networking_log("UrsinaNetworkingServer", "__init__", f"Cannot create the server : {e}")

    def process_net_events(self):
        self.events_manager.process_net_events()

    def get_client_id(self, Client_):
        for Client in self.clients:
            if Client.socket == Client_:
                return Client.id
        return None

    def get_clients_ids(self):
        Ret = []
        for Client in self.clients:
            Ret.append(Client.id)
        return Ret

    def get_client(self, Client_):
        for Client in self.clients:
            if Client.socket == Client_:
                return Client
        return None

    def get_clients(self):
        return self.clients

    def broadcast(self, Message_, Content_, IgnoreList = []):
        for Client in self.clients:
            if not Client in IgnoreList:
                Client.send_message(Message_, Content_)

    def handle(self, Client_):
        while True:
            try:
                self.network_buffer.receive_datagrams(Client_)

                for datagram in self.network_buffer.datagrams:

                    self.events_manager.push_event(datagram["Message"], self.get_client(Client_), datagram["Content"])

                self.network_buffer.datagrams = []

            except ConnectionError as e:
                ClientCopy = self.get_client(Client_)
                for Client in self.clients:
                    if Client.socket == Client_:
                        self.clients.remove(Client)
                        break

                self.events_manager.push_event(BUILTIN_EVENT_CLIENT_DISCONNECTED, ClientCopy)
                Client_.close()
                break

            except Exception as e:
                ursina_networking_log("UrsinaNetworkingServer", "handle", f"unknown error : {e}")
                break

    def receive(self):

        while True:

            client, address = self.server.accept()

            self.clients.append(UrsinaNetworkingConnectedClient(client, address, len(self.clients)))

            self.events_manager.push_event(BUILTIN_EVENT_CLIENT_CONNECTED, self.get_client(client))

            self.handle_thread = threading.Thread(target = self.handle, args = (client,))
            self.handle_thread.start()

class UrsinaNetworkingClient():

    def __init__(self, Ip_, Port_):

            try:
                self.connected = False
                self.lock = threading.Lock()
                self.events_manager = UrsinaNetworkingEvents(self.lock)
                self.network_buffer = UrsinaNetworinkDatagramsBuffer()
                self.event = self.events_manager.event
                self.connected = False
                self.handle_thread = threading.Thread(target = self.handle, args = (Ip_, Port_,))
                self.handle_thread.start()
                self.lock = threading.Lock()
            except Exception as e:
                ursina_networking_log("UrsinaNetworkingClient", "__init__", f"Cannot connect to the server : {e}")

    def process_net_events(self):
        self.events_manager.process_net_events()

    def handle(self, Ip_, Port_):
            try:
                self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.connection_response = self.client.connect_ex((Ip_, Port_))

                if self.connection_response == 0:
                    self.connected = True
                    self.events_manager.push_event(BUILTIN_EVENT_CONNECTION_ESTABLISHED)

                    ursina_networking_log("UrsinaNetworkingClient", "handle", "Client connected successfully !")

                    while True:

                        try:

                            self.network_buffer.receive_datagrams(self.client)

                            for datagram in self.network_buffer.datagrams:
                                self.events_manager.push_event(datagram["Message"], datagram["Content"])

                            self.network_buffer.datagrams = []

                        except ConnectionError as e:
                            self.events_manager.push_event(BUILTIN_EVENT_CONNECTION_ERROR, e)
                            ursina_networking_log("UrsinaNetworkingClient", "handle", f"connectionError : {e}")
                            break
                        except Exception as e:
                            ursina_networking_log("UrsinaNetworkingClient", "handle", f"unknown error : {e}")
                            break
                else:
                    self.events_manager.push_event(BUILTIN_EVENT_CONNECTION_ERROR, self.connection_response)

            except Exception as e:
                self.events_manager.push_event("connectionError", e)
                ursina_networking_log("UrsinaNetworkingClient", "handle", f"Connection Error : {e}")

    def send_message(self, Message_, Content_):
        try:
            if self.connected:
                if (Encoded:=ursina_networking_encode_message(Message_, Content_))==b"": return False
                self.client.sendall(Encoded)
                return True
            else:
                ursina_networking_log("UrsinaNetworkingClient", "send_message", f"WARNING : You are trying to send a message but the socket is not connected !")
        except Exception as e:
            ursina_networking_log("UrsinaNetworkingClient", "send_message", e)
            return False