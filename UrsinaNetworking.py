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
import time

HEADERSIZE = 10
MESSAGE_LENGTH = 8
BUFFERSIZE = 4096

def ursina_networking_encode_file(Path_):
    file = open(Path_, "rb")
    datas = file.read()
    file.close()
    return datas

def ursina_networking_log(Class_, Context_, Message_):
    print(f"[{Class_} / {Context_}] {Message_}")

def ursina_networking_encode_message(Message_):
    try:
        EncodedMessage = pickle.dumps(Message_)
        MessageLength = len(EncodedMessage)
        LengthToBytes = MessageLength.to_bytes(MESSAGE_LENGTH, byteorder = "big")
        FinalMessage = LengthToBytes + EncodedMessage
        return FinalMessage
    except Exception as e:
        ursina_networking_log("UrsinaNetworkingEncodeMessage", "func", e)
    return b""

class UrsinaNetworinkDatagramsBuffer():
    def __init__(self):
        self.header = bytes()
        self.payload = bytes()
        self.buf = bytearray()
        self.pickled_datas = None
        self.payload_length = 0
        self.receive_all = False
        self.datagrams = []
        self.STATE_HEADER = "STATE_HEADER"
        self.STATE_PAYLOAD = "STATE_PAYLOAD"
        self.state = self.STATE_HEADER

    def receive_datagrams(self, client_):

        self.buf += client_.recv(BUFFERSIZE)

        while True:

            self.state_changed = False

            if self.state == self.STATE_HEADER:

                if len(self.buf) >= MESSAGE_LENGTH:

                    self.header = self.buf[:MESSAGE_LENGTH]

                    del self.buf[:MESSAGE_LENGTH]

                    self.payload_length = int.from_bytes(self.header, byteorder = "big", signed = False)

                    self.state = self.STATE_PAYLOAD
                    self.state_changed = True

            elif self.state == self.STATE_PAYLOAD:

                if len(self.buf) >= self.payload_length:

                    self.payload = self.buf[:self.payload_length]

                    del self.buf[:self.payload_length]

                    self.state = self.STATE_HEADER
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

class UrsinaNetworkingEvents():

    def __init__(self):
        self.handlers = {}

    def call(self, type, *args):
        if type in self.handlers:
            for h in self.handlers[type]:
                h(*args)

    def event(self, func):
        self.handlers[func.__name__] = [func]

class UrsinaNetworkingPlayer():

    def __init__(self, socket, address, id):
        self.socket = socket
        self.address = address
        self.id = id
        self.name = f"Player {id}"
        self.datas = {}

    def __repr__(self):
        return self.name

    def send_message(self, Message_, Content_):
        try:
            NewMsg = {
                "Message"   :   Message_,
                "Content"   :   Content_
            }

            Encoded = ursina_networking_encode_message(NewMsg)
            self.socket.sendall(Encoded)
            return True
        except Exception as e:
            ursina_networking_log("UrsinaNetworkingPlayer", "send_message", e)
            return False

class UrsinaNetworkingServer():

    def __init__(self, Ip_, Port_):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((Ip_, Port_))
        self.server.listen()
        self.clients = []
        self.receiveThread = threading.Thread(target = self.receive)
        self.receiveThread.start()
        self.events = UrsinaNetworkingEvents()
        self.network_buffer = UrsinaNetworinkDatagramsBuffer()
        self.event = self.events.event

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
                    self.events.call(datagram["Message"], self.get_client(Client_), datagram["Content"])
                
                self.network_buffer.datagrams = []

            except:
                ClientCopy = self.get_client(Client_)
                for Client in self.clients:
                    if Client.socket == Client_:
                        self.clients.remove(Client)
                        break
                self.events.call("playerDisconnected", ClientCopy)
                Client_.close()
                break

    def receive(self):

        host, port = self.server.getsockname()

        ursina_networking_log("UrsinaNetworkingServer", "receive", "Server started !")
        ursina_networking_log("UrsinaNetworkingServer", "receive", f"Ip   :   {host}")
        ursina_networking_log("UrsinaNetworkingServer", "receive", f"Port :   {port}")
        
        while True:

            client, address = self.server.accept()

            self.clients.append(UrsinaNetworkingPlayer(client, address, len(self.clients)))
            ply = self.get_client(client)

            self.events.call("playerConnected", ply)

            self.handle_thread = threading.Thread(target = self.handle, args = (client,))
            self.handle_thread.start()

class UrsinaNetworkingClient():

    def __init__(self, Ip_, Port_):
            self.connected = False
            self.events = UrsinaNetworkingEvents()
            self.network_buffer = UrsinaNetworinkDatagramsBuffer()
            self.event = self.events.event
            self.connected = False
            self.handle_thread = threading.Thread(target = self.handle, args = (Ip_, Port_,))
            self.handle_thread.start()

    def handle(self, Ip_, Port_):
            try:
                self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.connection_response = self.client.connect_ex((Ip_, Port_))

                if self.connection_response == 0:
                    self.connected = True 
                    self.events.call("connectionEtablished")
                    ursina_networking_log("UrsinaNetworkingClient", "handle_thread", "Client connected successfully !")

                    while True:

                        try:

                            self.network_buffer.receive_datagrams(self.client)

                            for datagram in self.network_buffer.datagrams:
                                self.events.call(datagram["Message"], datagram["Content"])
                            
                            self.network_buffer.datagrams = []

                        except Exception as e:
                            self.events.call("connectionError", e)
                            ursina_networking_log("UrsinaNetworkingClient", "handle / receive", f"Receive Error : {e}")
                            break
                else:
                    self.events.call("connectionError", self.connection_response)

            except Exception as e:
                self.events.call("connectionError", e)
                ursina_networking_log("UrsinaNetworkingClient", "handle", f"Connection Error : {e}")

    def send_message(self, Message_, Content_):
        try:
            NewMsg = {
                "Message"   :   Message_,
                "Content"   :   Content_
            }
            encoded_message = ursina_networking_encode_message(NewMsg)
            self.client.sendall(encoded_message)
            return True
        except Exception as e:
            ursina_networking_log("UrsinaNetworkingClient", "send_message", e)
            return False