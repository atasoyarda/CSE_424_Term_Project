class TransactionPool:
    def __init__(self):
        self.transactions = []

    def addTransaction(self, transaction):
        self.transactions.append(transaction)

    def transactionExists(self, transaction):
        return any(
            poolTransaction.equals(transaction) for poolTransaction in self.transactions
        )

    def removeFromPool(self, transactions):
        self.transactions = [
            poolTransaction
            for poolTransaction in self.transactions
            if not any(
                poolTransaction.equals(transaction) for transaction in transactions
            )
        ]

    def forgingRequired(self):
        return len(self.transactions) >= 1
