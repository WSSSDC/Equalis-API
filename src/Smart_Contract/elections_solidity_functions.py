import os
import json
from web3 import Web3
from dotenv import load_dotenv


load_dotenv()
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

web3.eth.defaultAccount = web3.eth.accounts[0]

with open("src/Smart_Contract/deployment/compile_sol.json", 'r') as f:
    compile_sol = json.loads(f.read())

abi = compile_sol["contracts"]["elections.sol"]["ElectionsContract"]["abi"]

with open("src/Smart_Contract/deployment/address.json", 'r') as f:
    address_file = json.loads(f.read())

address = address_file["ADDRESS"]


contract = web3.eth.contract(
    address=address,
    abi=abi,
)


def getElectionsCount():
    return contract.functions.getElectionsCount().call()

# Create a election


def createElection(name):
    contract.functions.createElection(name).transact()
    return contract.functions.createElection(name).call()

# Create Candidate


def createCandidate(election_id, candidate_id, name, description):
    contract.functions.createCandidate(
        election_id, candidate_id, name, description).transact()
    return contract.functions.createCandidate(name).call()


print(createCandidate(2, "bram", "nam", "perfect"))


# Vote
# Start Election
# End Election
# Get Elections Count (Amount of elections Created)
# Get Election Name
# Get Election Total Votes
# Get Election Candidate Count (Number of candidates)
# Get Candidate Name
# Get Candidate Description
# Get Candidate Vote count
