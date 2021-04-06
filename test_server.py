from UrsinaNetworking import UrsinaNetworkingServer

Server = UrsinaNetworkingServer("localhost", 25565)

@Server.event
def HelloFromClient(Player, C):
    print(f"Receveid hello from {Player}")
    Player.send_message("HelloFromServer", f"Hey {Player} how are you ? :D")
    Server.broadcast("Broadcast", Server.get_clients_ids())