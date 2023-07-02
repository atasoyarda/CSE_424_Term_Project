import threading
import time
from Message import Message
from BlockchainUtils import BlockchainUtils


class PeerDiscoveryHandler:
    def __init__(self, node):
        self.socketCommunication = node

    def start(self):
        threading.Thread(target=self.status, args=()).start()
        threading.Thread(target=self.discovery, args=()).start()

    def status(self):
        while True:
            print("Current Connections:")
            print(
                "\n".join(
                    [
                        f"{peer.ip}:{peer.port}"
                        for peer in self.socketCommunication.peers
                    ]
                )
            )
            time.sleep(5)

    def discovery(self):
        while True:
            self.socketCommunication.broadcast(self.handshakeMessage())
            time.sleep(10)

    def handshake(self, connected_node):
        self.socketCommunication.send(connected_node, self.handshakeMessage())

    def handshakeMessage(self):
        message = Message(
            self.socketCommunication.socketConnector,
            "DISCOVERY",
            self.socketCommunication.peers,
        )
        return BlockchainUtils.encode(message)

    def handleMessage(self, message):
        peersSocketConnector = message.senderConnector
        peersPeerList = message.data

        if not any(
            peer.equals(peersSocketConnector) for peer in self.socketCommunication.peers
        ):
            self.socketCommunication.peers.append(peersSocketConnector)

        for peersPeer in peersPeerList:
            if not any(
                peer.equals(peersPeer) for peer in self.socketCommunication.peers
            ) and not peersPeer.equals(self.socketCommunication.socketConnector):
                self.socketCommunication.connect_with_node(peersPeer.ip, peersPeer.port)
