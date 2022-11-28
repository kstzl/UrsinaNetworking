<img src="https://raw.githubusercontent.com/kstzl/UrsinaNetworking/main/UrsinaNetworking_banner.png" width="500">

A Event-Based, high level API for networking !

## Installation
```
pip install ursinanetworking
```

## Creating a server
```python
from ursinanetworking import *

Server = UrsinaNetworkingServer("localhost", 25565)
```

## Creating a client
```python
from ursinanetworking import *

Client = UrsinaNetworkingClient("localhost", 25565)
```

## Built-in Server Events
```python
@Server.event
def onClientConnected(Client):
    print(f"{Client} connected !")

@Server.event
def onClientDisconnected(Client):
    print(f"{Client} disconnected !")
```

## Built-in Client Events
```python
@Client.event
def onConnectionEstablished():
    print("I'm connected to the server !")

@Client.event
def onConnectionError(Reason):
    print(f"Error ! Reason : {Reason}")
```

## Server to Client
### Server :
```python
from ursinanetworking import *

Server = UrsinaNetworkingServer("localhost", 25565)

@Server.event
def onClientConnected(Client):
    Client.send_message("HelloFromServer", f"Hello {Client} how are you ?! :D")

while True:
    Server.process_net_events()
```
### Client :
```python
from ursinanetworking import *

Client = UrsinaNetworkingClient("localhost", 25565)

@Client.event
def HelloFromServer(Content):
    print(f"Server says : {Content}")

while True:
    Client.process_net_events()
```

## Client to Server
### Client :
```python
from ursinanetworking import *

Client = UrsinaNetworkingClient("localhost", 25565)

@Client.event
def onConnectionEtablished():
    Client.send_message("HelloFromClient", "Hello, how are you ?")

while True:
    Client.process_net_events()
```
### Server :
```python
from ursinanetworking import *

Server = UrsinaNetworkingServer("localhost", 25565)

@Server.event
def HelloFromClient(Client, Content):
    print(f"{Client} says : {Content}")

while True:
    Server.process_net_events()
```

## Broadcasting
```python
from ursinanetworking import *

Server = UrsinaNetworkingClient("localhost", 25565)
Server.broadcast("HelloFromServer", "blabla")

while True:
    Server.process_net_events()
```

## Sending a file
### Server :
```python
from ursinanetworking import *

Server = UrsinaNetworkingServer("localhost", 25565)

@Server.event
def onClientConnected(Client):
    Client.send_message("receiveFile", ursina_networking_encode_file("my_image.png"))
```

### Client :
```python
from ursinanetworking import *

Client = UrsinaNetworkingClient("localhost", 25565)

@Client.event
def receiveFile(Content):
    f = open("receveid_image.png", "wb")
    f.write(ursina_networking_decompress_file(Content))
    f.close()
```
