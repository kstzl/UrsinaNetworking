<img src="https://raw.githubusercontent.com/kstzl/UrsinaNetworking/main/UrsinaNetworking_icon.png" width="64">
A high level API for networking with the Ursina Engine

## Creating a server
```python
from UrsinaNetworking import UrsinaNetworkingServer

Server = UrsinaNetworkingServer("localhost", 25565)
```

## Creating a client
```python
from UrsinaNetworking import UrsinaNetworkingClient

Client = UrsinaNetworkingClient("localhost", 25565)
```

## Client to Server
### Client :
```python
from UrsinaNetworking import UrsinaNetworkingClient

Client = UrsinaNetworkingClient("localhost", 25565)
Client.send_message("HelloFromClient", "blabla")
```
### Server :
```python
from UrsinaNetworking import UrsinaNetworkingServer

Server = UrsinaNetworkingServer("localhost", 25565)

@Server.event
def HelloFromClient(Sender, Content):
    print(f"{Sender} said : {Content}")
```

## Server to Client
### Server :
```python
from UrsinaNetworking import UrsinaNetworkingServer

Server = UrsinaNetworkingClient("localhost", 25565)
Server.send_message("HelloFromServer", "blabla")
```
### Client :
```python
from UrsinaNetworking import UrsinaNetworkingClient

Client = UrsinaNetworkingClient("localhost", 25565)

@Client.event
def HelloFromServer(Content):
    print(f"Server said : {Content}")
```

## Broadcasting
```python
from UrsinaNetworking import UrsinaNetworkingServer

Server = UrsinaNetworkingClient("localhost", 25565)
Server.broadcast("HelloFromServer", "blabla")
```
