from Transaction import Transaction
from Wallet import Wallet
from TransactionPool import TransactionPool
from Block import Block
from Blockchain import Blockchain
from BlockchainUtils import BlockchainUtils
import pprint

if __name__ == '__main__':
    # Create two wallets
    senderWallet = Wallet()
    receiverWallet = Wallet()

    # Create a transaction
    transaction = senderWallet.createTransaction(receiverWallet.publicKeyString(), 100, 'EXCHANGE')

    # Create a TransactionPool
    transactionPool = TransactionPool()

    # Add the transaction to the TransactionPool
    transactionPool.addTransaction(transaction)

    # Create a new block
    lastHash = BlockchainUtils.hash(Block.genesis().payload()).hexdigest()
    block = senderWallet.createBlock([transaction], lastHash, 1) 

    # Create a new blockchain and add the block
    blockchain = Blockchain()
    blockchain.addBlock(block)

    # Print the state of the blockchain
    pprint.pprint(blockchain.toJson())
