from PySide2.QtCore import QTimer
from ursinanetworking import *
from PySide2.QtWidgets import *
import sys

#---NETWORKING---
Client = UrsinaNetworkingClient("localhost", 25565)

@Client.event
def receive_message(datas):
    global messages
    messages.append(f"<b>{datas['author']} :</b> {datas['message']}")

@Client.event
def clear_chat(datas):
    global messages
    messages.clear()

@Client.event
def get_identity(datas):
    global window
    window.setWindowTitle(f"{window.windowTitle()} ({datas['name']})")

def process_network():
    Client.process_net_events()

#---GUI EVENTS---
def send_message():
    global message
    Client.send_message("send_message", message.text())
    message.setText("")

#---GUI---
app = QApplication()

messages = QTextBrowser()
messages.append("Bienvenue sur le chat. Pour commencer, veuillez indiquer votre pseudo avec la barre ci-dessous.")

message = QLineEdit()
message.returnPressed.connect(send_message)

layout = QVBoxLayout()

layout.addWidget(messages)
layout.addWidget(message)

timer = QTimer()

timer.timeout.connect(process_network)

timer.start(100)

window = QWidget()
window.setLayout(layout)
window.setWindowTitle("QTChat")
window.show()

sys.exit(app.exec_())