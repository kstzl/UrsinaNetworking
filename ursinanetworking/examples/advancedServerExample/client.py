"""
This Example demonstrates implementing a function which 
can return data after requesting it from the server!!!
"""
from ursinanetworking import*

ADDRESS = ("localhost", 12345)

# python -m advancedServerExample.client


class Client:
    def __init__(self, address) -> None:
        # temporarily stores messages to be sent!
        self.messagesToSend = {}  # { Message_ : Content_ }
        
        self.ursinaClient = UrsinaNetworkingClient(*address)
        self.start_events_processing_thread()

        @self.ursinaClient.event
        def onConnectionEtablished():
            self.StartSendMessageThread()

        dataRecvd = self.requestDataFromServer()
        print("Data Len Received: ", len(dataRecvd))

    def requestDataFromServer(self):
        """
        An example of requesting Something!

        Returns:
            [bytes]: data that you asked for!
        """
        self.tempVar = None
        dataAvailable = threading.Event()

        self.sendMessage("requestData", "")

        @self.ursinaClient.event
        def receiveData(Content):
            self.ursinaClient.lock.acquire()

            self.tempVar = Content
            dataAvailable.set()

            self.ursinaClient.lock.release()

            # print("Len Data Recvd: ", len(Content))

        dataAvailable.wait()

        tempVar = self.tempVar

        del self.tempVar
        return tempVar

    def start_events_processing_thread(self):
        """
        Process events concurrently!
        """
        def process_net_events():
            while True:
                self.ursinaClient.process_net_events()
        self.processEventsThread = threading.Thread(target=process_net_events)
        self.processEventsThread.start()

    def StartSendMessageThread(self):
        """
        Sends messages concurrently!
        """
        def messageSending():
            while True:
                for message, content in self.messagesToSend.items():
                    self.ursinaClient.send_message(message, content)
                self.messagesToSend.clear()

        messagingThread = threading.Thread(target=messageSending)
        messagingThread.start()

    def sendMessage(self, Message_, Content_):
        """
        Use this instead of self.ursinaClient to send messages!

        Args:
            Message_ (str): name of function to call on the server side!
            Content_ (Any): actual message data!
        """
        self.messagesToSend[Message_] = Content_

if __name__ == "__main__":
    c = Client(ADDRESS)
