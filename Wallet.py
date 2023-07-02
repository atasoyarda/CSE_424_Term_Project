from Crypto.PublicKey import RSA
from Transaction import Transaction
from Block import Block
from BlockchainUtils import BlockchainUtils
from Crypto.Signature import PKCS1_v1_5


class Wallet():
    def __init__(self):
        self.keyPair = RSA.generate(2048)

    def fromKey(self, file):
        with open(file, 'r') as keyfile:
            key = RSA.importKey(keyfile.read())
        self.keyPair = key

    def sign(self, data):
        dataHash = BlockchainUtils.hash(data)
        signature = PKCS1_v1_5.new(self.keyPair).sign(dataHash)
        return signature.hex()

    @staticmethod
    def signatureValid(data, signature, publicKeyString):
        signature = bytes.fromhex(signature)
        dataHash = BlockchainUtils.hash(data)
        publicKey = RSA.importKey(publicKeyString)
        return PKCS1_v1_5.new(publicKey).verify(dataHash, signature)

    def publicKeyString(self):
        return self.keyPair.publickey().exportKey('PEM').decode('utf-8')

    def createTransaction(self, receiver, amount, type):
        transaction = Transaction(self.publicKeyString(), receiver, amount, type)
        transaction.sign(self.sign(transaction.payload()))
        return transaction
        
    def createBlock(self, transactions, lastHash, blockCount):
        block = Block(transactions, lastHash, self.publicKeyString(), blockCount)
        block.sign(self.sign(block.payload()))
        return block
