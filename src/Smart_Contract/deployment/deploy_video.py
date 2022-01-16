import json

from web3 import Web3

# In the video, we forget to `install_solc`
# from solcx import compile_standard
from solcx import compile_standard, install_solc
import os
from dotenv import load_dotenv

load_dotenv()


with open("src/Smart_Contract/elections.sol", "r") as file:
    election_file = file.read()

# We add these two lines that we forgot from the video!
print("Installing...")
install_solc("0.8.0")

# Solidity source code
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"elections.sol": {"content": election_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.8.0",
)

with open("compiled_sol.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["elections.sol"]["ElectionsContract"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = json.loads(
    compiled_sol["contracts"]["elections.sol"]["ElectionsContract"]["metadata"]
)["output"]["abi"]

w3 = Web3(
    Web3.HTTPProvider("https://rinkeby.infura.io/v3/1f9910d7cd1c4ed2ac44ec87f3d2a4e3")
)
chain_id = 4

# For connecting to ganache
# w3 = Web3(Web3.HTTPProvider("http://0.0.0.0:8545"))
# chain_id = 1337
my_address = "0x11102570851b674029C7b90282A2470aFA89f31f"
private_key = "0x44e01920e7a6865970bef5350001b9b67cb20346990ead8cca1745bda743e73b"

# Create the contract in Python
Election = w3.eth.contract(abi=abi, bytecode=bytecode)
# Get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)
# Submit the transaction that deploys the contract
transaction = Election.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)
# Sign the transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
print("Deploying Contract!")
# Send it!
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
# Wait for the transaction to be mined, and get the transaction receipt
print("Waiting for transaction to finish...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Done! Contract deployed to {tx_receipt.contractAddress}")


# Working with deployed Contracts


contract = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)


print("Default elections: {}".format(contract.functions.getElectionsCount().call()))

# update the greeting
tx_hash = contract.functions.createElection("First Erection").transact()

# Wait for transaction to be mined...
w3.eth.waitForTransactionReceipt(tx_hash)

# Display the new greeting value
print("Updated elections: {}".format(contract.functions.getElectionsCount().call()))


# print(f"Initial Stored Value {contract.functions.retrieve().call()}")
# greeting_transaction = contract.functions.store(15).buildTransaction(
#     {
#         "chainId": chain_id,
#         "gasPrice": w3.eth.gas_price,
#         "from": my_address,
#         "nonce": nonce + 1,
#     }
# )

# signed_greeting_txn = w3.eth.account.sign_transaction(
#     greeting_transaction, private_key=private_key
# )
# tx_greeting_hash = w3.eth.send_raw_transaction(signed_greeting_txn.rawTransaction)
# print("Updating stored Value...")
# tx_receipt = w3.eth.wait_for_transaction_receipt(tx_greeting_hash)

# print(contract.functions.retrieve().call())
