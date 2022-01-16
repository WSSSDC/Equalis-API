import json

from web3 import Web3

# from solcx import compile_standard
from solcx import compile_standard, install_solc
import os
from dotenv import load_dotenv

load_dotenv()

# If local true uses Ganache otherwise uses rinkeby tesnet
isLocal = False

if isLocal:
    URL = "http://127.0.0.1:7545"
    CHAIN_ID = 1337
    WALLET_ADDRESS = "0xF9Aa14b7d27C84aCAffcdE6d264359C7a3DFc39a"
    PRIVATE_KEY = os.getenv("PRIVATE_KEY_GANACHE")
else:
    URL = "https://rinkeby.infura.io/v3/1f9910d7cd1c4ed2ac44ec87f3d2a4e3"
    CHAIN_ID = 4
    WALLET_ADDRESS = "0x11102570851b674029C7b90282A2470aFA89f31f"
    PRIVATE_KEY = os.getenv("PRIVATE_KEY_TESTNET")


with open("src/Smart_Contract/elections.sol", "r") as file:
    election_file = file.read()

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

w3 = Web3(Web3.HTTPProvider(URL))


Election = w3.eth.contract(abi=abi, bytecode=bytecode)
# Get the latest transaction
nonce = w3.eth.getTransactionCount(WALLET_ADDRESS)
# Submit the transaction that deploys the contract
transaction = Election.constructor().buildTransaction(
    {
        "chainId": CHAIN_ID,
        "gasPrice": w3.eth.gas_price,
        "from": WALLET_ADDRESS,
        "nonce": nonce,
    }
)

# Sign the transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=PRIVATE_KEY)
print("Deploying Contract!")
# Send it!
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
# Wait for the transaction to be mined, and get the transaction receipt
print("Waiting for transaction to finish...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Done! Contract deployed to {tx_receipt.contractAddress}")

# Working with deployed Contracts

CONTRACT_ADDRESS = tx_receipt.contractAddress

# Save the contract address
settings = {}
settings["CONTRACT_ADDRESS"] = CONTRACT_ADDRESS
settings["WALLET_ADDRESS"] = WALLET_ADDRESS
settings["CHAIN_ID"] = CHAIN_ID
settings["URL"] = URL
settings["ISLOCAL"] = isLocal


with open("src/Smart_Contract/deployment/settings.json", "w") as file:
    json.dump(settings, file)

# Create the contract
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)


print(f"Default elections: {contract.functions.getElectionsCount().call()}")


test = contract.functions.createElection("First Erection")

nonce = w3.eth.getTransactionCount(WALLET_ADDRESS)

transaction = test.buildTransaction(
    {
        "chainId": CHAIN_ID,
        "gasPrice": w3.eth.gas_price,
        "from": WALLET_ADDRESS,
        "nonce": nonce,
    }
)

signed_txn = w3.eth.account.sign_transaction(transaction, private_key=PRIVATE_KEY)
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
print("Waiting for transaction to finish...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Transaction finished!")

# Display the new greeting value
print("Updated elections: {}".format(contract.functions.getElectionsCount().call()))
print("First Election Name: {}".format(contract.functions.getElectionName(1).call()))
