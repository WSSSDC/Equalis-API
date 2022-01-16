import os
import json
from web3 import Web3
from dotenv import load_dotenv


load_dotenv()

with open("src/Smart_Contract/deployment/settings.json", "r") as f:
    settings = json.loads(f.read())


URL = settings["URL"]
WALLET_ADDRESS = settings["WALLET_ADDRESS"]
CONTRACT_ADDRESS = settings["CONTRACT_ADDRESS"]
CHAIN_ID = settings["CHAIN_ID"]
PRIVATE_KEY = "0x44e01920e7a6865970bef5350001b9b67cb20346990ead8cca1745bda743e73b"


w3 = Web3(Web3.HTTPProvider(URL))

with open("src/Smart_Contract/deployment/compile_sol.json", "r") as f:
    compile_sol = json.loads(f.read())

abi = compile_sol["contracts"]["elections.sol"]["ElectionsContract"]["abi"]


contract = w3.eth.contract(
    address=CONTRACT_ADDRESS,
    abi=abi,
)


def make_transaction(function_to_call):
    try:
        response = function_to_call.call()

        nonce = w3.eth.getTransactionCount(WALLET_ADDRESS)
        transaction = function_to_call.buildTransaction(
            {
                "chainId": CHAIN_ID,
                "gasPrice": w3.eth.gas_price,
                "from": WALLET_ADDRESS,
                "nonce": nonce,
            }
        )

        signed_txn = w3.eth.account.sign_transaction(
            transaction, private_key=PRIVATE_KEY
        )
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        print("Waiting for transaction to finish...")
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        return response
    except:
        return "Error occurred calling the blockchain"


# Create a election WORKS
def createElection(name):
    function_to_call = contract.functions.createElection(name)
    return make_transaction(function_to_call)


# Create Candidate WORKS
def createCandidate(election_id, name, description):
    function_to_call = contract.functions.createCandidate(
        election_id, name, description
    )
    return make_transaction(function_to_call)


# Start Election WORKS
def startElection(election_id):
    function_to_call = contract.functions.startElection(election_id)
    return make_transaction(function_to_call)


# End Election
def endElection(election_id):
    function_to_call = contract.functions.endElection(election_id)
    return make_transaction(function_to_call)


# Vote WORKS
def vote(election_id, candidate_id, user_id):
    function_to_call = contract.functions.vote(election_id, candidate_id, user_id)
    return make_transaction(function_to_call)


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
print(f'New ElectionID: {createElection("USA Election")}')
print(f"The election name: {getElectionName(2)}")
print(f'Candidate ID: {createCandidate(2, "Obama", "this is a nice guy")}')
print(f'Candidate ID: {createCandidate(2, "Joe Biden", "this is a old guy")}')
print(f'Candidate ID: {createCandidate(2, "Trump", "this is a stupid guy")}')

print(f"Start Election: {startElection(2)}")

print(f'Voting: {vote(2, 1, "connor")}')
print(f'Voting: {vote(2, 1, "rene")}')
print(f'Voting: {vote(2, 1, "bram")}')
print(f'Voting: {vote(2, 2, "arjun")}')

print(f"End Election: {endElection(2)}")

print(f"Obama Votes: {getCandidateVotes(2, 1)}")
print(f"Joe Biden Votes: {getCandidateVotes(2, 2)}")
print(f"Trump Votes: {getCandidateVotes(2, 3)}")


# print(getElectionCandidatesCount(1))


# print(f"Votes of the candidate: {getCandidateVotes(1, 2)}")
# print(hasVoted(1, "popo"))

# print(getElectionName(1))

# print(getElectionName(3))
# print(getElectionName(4))
# print(getElectionName(5))
