import os
import json
from web3 import Web3
from dotenv import load_dotenv


load_dotenv()
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

web3.eth.defaultAccount = web3.eth.accounts[0]

with open("src/Smart_Contract/deployment/compile_sol.json", "r") as f:
    compile_sol = json.loads(f.read())

abi = compile_sol["contracts"]["elections.sol"]["ElectionsContract"]["abi"]

with open("src/Smart_Contract/deployment/address.json", "r") as f:
    address_file = json.loads(f.read())

address = address_file["ADDRESS"]


contract = web3.eth.contract(
    address=address,
    abi=abi,
)


# Create a election WORKS
def createElection(name):
    contract.functions.createElection(name).transact()
    return contract.functions.createElection(name).call()


# Create Candidate WORKS
def createCandidate(election_id, name, description):
    contract.functions.createCandidate(election_id, name, description).transact()
    return contract.functions.createCandidate(election_id, name, description).call()


# Start Election WORKS
def startElection(election_id):
    contract.functions.startElection(election_id).transact()
    return contract.functions.startElection(election_id).call()


# End Election
def endElection(election_id):
    contract.functions.endElection(election_id).transact()
    return contract.functions.endElection(election_id).call()


# Vote WORKS
def vote(election_id, candidate_id, user_id):
    return contract.functions.vote(election_id, candidate_id, user_id).call()


# Get Elections Count (Amount of elections Created) WORKS
def getElectionsCount():
    return contract.functions.getElectionsCount().call()


# Get Election Status (0 for Created, 1 for voting, 2 for ended) WORKS
def getElectionStatus(election_id):
    return contract.functions.getElectionStatus(election_id).call()


# Check if user has voted
def hasUserVoted(election_id, user_id):
    return contract.functions.hasUserVoted(election_id, user_id).call()


# Get Election Name
def getElectionName(election_id):
    contract.functions.getElectionName(election_id).transact()
    return contract.functions.getElectionName(election_id).call()


# Get Election Total Votes
def getElectionVotes(election_id):
    return contract.functions.getElectionVotes(election_id).call()


# Get Election Candidate Count (Number of candidates) WORKS
def getElectionCandidatesCount(election_id):
    return contract.functions.getElectionCandidatesCount(election_id).call()


# Get Number of votes per candidate WORKS
def getCandidateVotes(election_id, candidate_id):
    # contract.functions.getCandidateVotes(election_id, candidate_id).transact()
    return contract.functions.getCandidateVotes(election_id, candidate_id).call()


# Get Candidate Name
def getCandidateName(election_id, candidate_id):
    return contract.functions.getCandidateName(election_id, candidate_id).call()


# Get Candidate Description
def getCandidateDescription(election_id, candidate_id):
    return contract.functions.getCandidateDescription(election_id, candidate_id).call()


print(f"Election Status: {getElectionStatus(1)}")
# print(getElectionsCount())
# print(createElection("us election"))
# print(f'Candidate ID: {createCandidate(1, "another one", "test")}')
# print(getElectionCandidatesCount(1))
# print(f"Start Election: {startElection(1)}")
# print(f'Voting: {vote(1, 2, "cuco")}')
# print(f"Votes of the candidate: {getCandidateVotes(1, 2)}")
# print(hasVoted(1, "popo"))

print(getElectionName(1))
print(getElectionName(2))
