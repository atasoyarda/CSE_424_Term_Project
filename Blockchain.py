from Block import Block
from BlockchainUtils import BlockchainUtils
from AccountModel import AccountModel
from ProofOfStake import ProofOfStake


class Blockchain:
    def __init__(self):
        self.blocks = [Block.genesis()]
        self.accountModel = AccountModel()
        self.pos = ProofOfStake()

    def addBlock(self, block):
        self.executeTransactions(block.transactions)
        self.blocks.append(block)

    def toJson(self):
        return {"blocks": [block.toJson() for block in self.blocks]}

    def blockCountValid(self, block):
        return self.blocks[-1].blockCount == block.blockCount - 1

    def lastBlockHashValid(self, block):
        latestBlockchainBlockHash = BlockchainUtils.hash(
            self.blocks[-1].payload()
        ).hexdigest()
        return latestBlockchainBlockHash == block.lastHash

    def getCoveredTransactionSet(self, transactions):
        return [
            transaction
            for transaction in transactions
            if self.transactionCovered(transaction)
        ]

    def transactionCovered(self, transaction):
        if transaction.type == "EXCHANGE":
            return True
        return (
            self.accountModel.getBalance(transaction.senderPublicKey)
            >= transaction.amount
        )

    def executeTransactions(self, transactions):
        for transaction in transactions:
            self.executeTransaction(transaction)

    def executeTransaction(self, transaction):
        sender = transaction.senderPublicKey
        receiver = transaction.receiverPublicKey
        amount = transaction.amount
        self.accountModel.updateBalance(sender, -amount)
        if transaction.type == "STAKE" and sender == receiver:
            self.pos.update(sender, amount)
        else:
            self.accountModel.updateBalance(receiver, amount)

    def nextForger(self):
        lastBlockHash = BlockchainUtils.hash(self.blocks[-1].payload()).hexdigest()
        return self.pos.forger(lastBlockHash)

    def createBlock(self, transactionsFromPool, forgerWallet):
        coveredTransactions = self.getCoveredTransactionSet(transactionsFromPool)
        self.executeTransactions(coveredTransactions)
        newBlock = forgerWallet.createBlock(
            coveredTransactions,
            BlockchainUtils.hash(self.blocks[-1].payload()).hexdigest(),
            len(self.blocks),
        )
        self.blocks.append(newBlock)
        return newBlock

    def transactionExists(self, transaction):
        return any(
            transaction.equals(blockTransaction)
            for block in self.blocks
            for blockTransaction in block.transactions
        )

    def forgerValid(self, block):
        return self.pos.forger(block.lastHash) == block.forger

    def transactionsValid(self, transactions):
        return len(self.getCoveredTransactionSet(transactions)) == len(transactions)
