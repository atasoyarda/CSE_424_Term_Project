import time
import copy

class Block:
    def __init__(self, transactions, lastHash, forger, blockCount):
        self.blockCount = blockCount
        self.transactions = transactions
        self.lastHash = lastHash
        self.timestamp = time.time()
        self.forger = forger
        self.signature = ''

    @staticmethod
    def genesis():
        genesisBlock = Block([], 'genesisHash', 'genesis', 0)
        genesisBlock.timestamp = 0
        return genesisBlock

    def toJson(self):
        return {
            'blockCount': self.blockCount,
            'lastHash': self.lastHash,
            'signature': self.signature,
            'forger': self.forger,
            'timestamp': self.timestamp,
            'transactions': [transaction.toJson() for transaction in self.transactions]
        }

    def payload(self):
        jsonRepresentation = self.toJson().copy()
        jsonRepresentation['signature'] = ''
        return jsonRepresentation

    def sign(self, signature):
        self.signature = signature
