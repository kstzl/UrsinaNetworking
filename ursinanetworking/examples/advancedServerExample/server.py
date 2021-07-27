from ursinanetworking import*
# import threading
import secrets

ADDRESS = ("localhost", 12345)

# python -m advancedServerExample.server 

class Server:
    def __init__(self, address) -> None:
        self.data = secrets.token_bytes(1000)
        self.ursinaServer = UrsinaNetworkingServer(*address)
        self.start_events_processing_thread()

        @self.ursinaServer.event
        def requestData(Client, Content):
            print("OK I will send you the Data!", len(self.data), "bytes")
            Client.send_message("receiveData", self.data)

    def start_events_processing_thread(self):
        def process_net_events():
            while True:
                self.ursinaServer.process_net_events()
        self.processEventsThread = threading.Thread(target=process_net_events)
        self.processEventsThread.start()


if __name__ == "__main__":
    c = Server(ADDRESS)