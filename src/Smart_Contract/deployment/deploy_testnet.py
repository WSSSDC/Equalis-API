import json
from re import S
from solcx import compile_standard, install_solc
from web3 import Web3
import os
from dotenv import load_dotenv

install_solc("0.8.2")
load_dotenv()


CONTRACT_PATH = "src/Smart_Contract/elections.sol"
with open(CONTRACT_PATH, "r") as f:
    source = f.read()

# Compile Solidity

compile_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"elections.sol": {"content": source}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.8.2",
)

with open("src/Smart_Contract/deployment/compile_sol.json", "w") as file:
    json.dump(compile_sol, file)

bytecode = compile_sol["contracts"]["elections.sol"]["ElectionsContract"]["evm"][
    "bytecode"
]["object"]
abi = compile_sol["contracts"]["elections.sol"]["ElectionsContract"]["abi"]


url = "https://rinkeby.infura.io/v3/1f9910d7cd1c4ed2ac44ec87f3d2a4e3"
w3 = Web3(Web3.HTTPProvider(url))

chain_id = 4
wallet_address = "0x11102570851b674029C7b90282A2470aFA89f31f"
private_key = "0x44e01920e7a6865970bef5350001b9b67cb20346990ead8cca1745bda743e73b"

contract = w3.eth.contract(abi=abi, bytecode=bytecode)
# print("Elections")

# nonce = web3.eth.getTransactionCount(address)
# print("Nonce")

# transaction = Elections.constructor().buildTransaction(
#     {"chainId": chain_id, "from": address, "nonce": nonce}
# )
# print("Transaction")
# signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)
# print("Deploying contract...")

# tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
# tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
# print("Deployed!")

from web3.middleware import geth_poa_middleware

w3.middleware_onion.inject(geth_poa_middleware, layer=0)

nonce = w3.eth.get_transaction_count(wallet_address)

transaction = contract.constructor().buildTransaction(
    {"chainId": chain_id, "from": wallet_address, "nonce": nonce}
)

# transaction.update({"gas": appropriate_gas_amount})
transaction.update({"nonce": nonce})
signed_tx = w3.eth.account.sign_transaction(transaction, private_key)

txn_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
print(f"Hash: {txn_hash}")
txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
# print(txn_receipt)
print("Deployed!")

contract = w3.eth.contract(address=txn_receipt.contractAddress, abi=abi)

print("Default elections: {}".format(contract.functions.getElectionsCount().call()))


tx_hash = contract.functions.createElection("First Election").transact()

# Wait for transaction to be mined...
# w3.eth.waitForTransactionReceipt(tx_hash)

# # Display the new greeting value
# print("Updated elections: {}".format(contract.functions.getElectionsCount().call()))
