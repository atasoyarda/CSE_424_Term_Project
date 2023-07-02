from Blockchain import Blockchain
from TransactionPool import TransactionPool
from Wallet import Wallet
from SocketCommunication import SocketCommunication
from NodeAPI import NodeAPI
from Message import Message
from BlockchainUtils import BlockchainUtils
import copy


class Node:
    def __init__(self, ip, port, key=None):
        self.p2p = None
        self.ip = ip
        self.port = port
        self.blockchain = Blockchain()
        self.transactionPool = TransactionPool()
        self.wallet = Wallet()
        if key is not None:
            self.wallet.fromKey(key)

    def startP2P(self):
        self.p2p = SocketCommunication(self.ip, self.port)
        self.p2p.startSocketCommunication(self)


    def startAPI(self, apiPort):
        self.api = NodeAPI()
        self.api.injectNode(self)
        self.api.start(apiPort)

    def handleTransaction(self, transaction):
        signatureValid = Wallet.signatureValid(
            transaction.payload(), transaction.signature, transaction.senderPublicKey
        )
        if not any(
            [
                self.transactionPool.transactionExists(transaction),
                self.blockchain.transactionExists(transaction),
                not signatureValid,
            ]
        ):
            self.transactionPool.addTransaction(transaction)
            encodedMessage = BlockchainUtils.encode(
                Message(self.p2p.socketConnector, "TRANSACTION", transaction)
            )
            self.p2p.broadcast(encodedMessage)
            if self.transactionPool.forgingRequired():
                self.forge()

    def handleBlock(self, block):
        forger = block.forger
        blockHash = block.payload()
        signature = block.signature
        if not self.blockchain.blockCountValid(block):
            self.requestChain()
        if all(
            [
                self.blockchain.lastBlockHashValid(block),
                self.blockchain.forgerValid(block),
                self.blockchain.transactionsValid(block.transactions),
                Wallet.signatureValid(blockHash, signature, forger),
            ]
        ):
            self.blockchain.addBlock(block)
            self.transactionPool.removeFromPool(block.transactions)
            self.p2p.broadcast(
                BlockchainUtils.encode(
                    Message(self.p2p.socketConnector, "BLOCK", block)
                )
            )

    def handleBlockchainRequest(self, requestingNode):
        self.p2p.send(
            requestingNode,
            BlockchainUtils.encode(
                Message(self.p2p.socketConnector, "BLOCKCHAIN", self.blockchain)
            ),
        )

    def handleBlockchain(self, blockchain):
        localBlockchainCopy = copy.deepcopy(self.blockchain)
        if len(localBlockchainCopy.blocks) < len(blockchain.blocks):
            for blockNumber, block in enumerate(blockchain.blocks):
                if blockNumber >= len(localBlockchainCopy.blocks):
                    localBlockchainCopy.addBlock(block)
                    self.transactionPool.removeFromPool(block.transactions)
            self.blockchain = localBlockchainCopy

    def forge(self):
        forger = self.blockchain.nextForger()
        if forger == self.wallet.publicKeyString():
            print("i am the forger")
            block = self.blockchain.createBlock(
                self.transactionPool.transactions, self.wallet
            )
            self.transactionPool.removeFromPool(self.transactionPool.transactions)
            self.p2p.broadcast(
                BlockchainUtils.encode(
                    Message(self.p2p.socketConnector, "BLOCK", block)
                )
            )
        else:
            print("i am not the forger")

    def requestChain(self):
        self.p2p.broadcast(
            BlockchainUtils.encode(
                Message(self.p2p.socketConnector, "BLOCKCHAINREQUEST", None)
            )
        )
