import json
from web3 import Web3

ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

with open("src/Smart_Contract/deployment/compile_sol.json", 'r') as f:
    compile_sol = json.loads(f.read())

abi = compile_sol["contracts"]["elections.sol"]["ElectionsContract"]["abi"]
address = web3.toChecksumAddress("0x711644A30f3DC3024A2165cAAabc24069E185F23")

contract = web3.eth.contract(address=address, abi=abi)

print(contract.functions.getElectionsCount().call())

# Create a election
# Create Candidate
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
