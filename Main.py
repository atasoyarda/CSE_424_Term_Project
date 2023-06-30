from Transaction import Transaction
from Wallet import Wallet
from TransactionPool import TransactionPool
from Block import Block
from Blockchain import Blockchain
from BlockchainUtils import BlockchainUtils
from AccountModel import AccountModel
import pprint

if __name__ == '__main__':
    blockchain = Blockchain()

    # İlk cüzdanlar oluşturulur
    aliye_wallet = Wallet()
    bora_wallet = Wallet()
    emre_wallet = Wallet()

    # Exchange işlemleri
    transaction_pool = TransactionPool()
    aliye_to_bora_transaction = aliye_wallet.createTransaction(bora_wallet.publicKeyString(), 100, 'EXCHANGE')
    bora_to_aliye_transaction = bora_wallet.createTransaction(aliye_wallet.publicKeyString(), 100, 'EXCHANGE')
    emre_to_aliye_transaction = emre_wallet.createTransaction(aliye_wallet.publicKeyString(), 100, 'EXCHANGE')
    transaction_pool.addTransaction(aliye_to_bora_transaction)
    transaction_pool.addTransaction(bora_to_aliye_transaction)
    transaction_pool.addTransaction(emre_to_aliye_transaction)

    # Blok oluşturulur ve zincire eklenir
    forger_wallet = Wallet()
    block1 = blockchain.createBlock(transaction_pool.transactions, forger_wallet)
    blockchain.addBlock(block1)
    transaction_pool.removeFromPool(block1.transactions)

    # TRANSFER ve STAKE işlemleri
    a_to_b_transfer = aliye_wallet.createTransaction(bora_wallet.publicKeyString(), 20, 'TRANSFER')
    b_to_e_transfer = bora_wallet.createTransaction(emre_wallet.publicKeyString(), 30, 'TRANSFER')
    e_stake = emre_wallet.createTransaction(emre_wallet.publicKeyString(), 50, 'STAKE')
    transaction_pool.addTransaction(a_to_b_transfer)
    transaction_pool.addTransaction(b_to_e_transfer)
    transaction_pool.addTransaction(e_stake)

    # Blok oluşturulur ve zincire eklenir
    block2 = blockchain.createBlock(transaction_pool.transactions, forger_wallet)
    blockchain.addBlock(block2)
    transaction_pool.removeFromPool(block2.transactions)

    # Bora, Aliye ve Emre kendi cüzdanlarına para aktarır
    b_self_transfer = bora_wallet.createTransaction(bora_wallet.publicKeyString(), 20, 'TRANSFER')
    a_self_transfer = aliye_wallet.createTransaction(aliye_wallet.publicKeyString(), 40, 'TRANSFER')
    e_self_transfer = emre_wallet.createTransaction(emre_wallet.publicKeyString(), 60, 'TRANSFER')
    transaction_pool.addTransaction(b_self_transfer)
    transaction_pool.addTransaction(a_self_transfer)
    transaction_pool.addTransaction(e_self_transfer)

    # Blok oluşturulur ve zincire eklenir
    block3 = blockchain.createBlock(transaction_pool.transactions, forger_wallet)
    blockchain.addBlock(block3)
    transaction_pool.removeFromPool(block3.transactions)

    # Sonuçları göster
    pprint.pprint(blockchain.toJson())
