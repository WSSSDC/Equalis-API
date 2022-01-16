import json
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

# Set up web3 connection with Ganache
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# set pre-funded account as sender
web3.eth.defaultAccount = web3.eth.accounts[0]

# Instantiate and deploy contract
Elections = web3.eth.contract(abi=abi, bytecode=bytecode)
print("Deploying Contract!")

# Submit the transaction that deploys the contract
tx_hash = Elections.constructor().transact()
print("Waiting for transaction to finish...")

# Wait for the transaction to be mined, and get the transaction receipt
tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
print("Done! Contract deployed to Ganache!")

# Create the contract instance with the newly-deployed address
contract = web3.eth.contract(
    address=tx_receipt.contractAddress,
    abi=abi,
)

save_file = {}
save_file["ADDRESS"] = tx_receipt.contractAddress

with open("src/Smart_Contract/deployment/address.json", "w") as file:
    json.dump(save_file, file)


print("Default elections: {}".format(contract.functions.getElectionsCount().call()))

# Create a new election
tx_hash = contract.functions.createElection("First Erection").transact()

# Wait for transaction to be mined...
print("Waiting for transaction to finish...")
web3.eth.waitForTransactionReceipt(tx_hash)
print("Transaction finished!")

# Display the new greeting value
print("Updated elections: {}".format(contract.functions.getElectionsCount().call()))
