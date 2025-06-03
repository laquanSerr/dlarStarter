from web3 import Web3
import hashlib
import json

# Connect to local Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))  # ✅ Use HTTP not HTTPS

# Confirm connection
if not w3.isConnected():
    raise ConnectionError("Web3 not connected.")

# Load ABI from a JSON file (assuming you have compiled contract in build folder)
with open('build/DADManager.json') as f:
    contract_json = json.load(f)
    abi = contract_json['abi']

# Replace with your actual deployed contract address from Ganache
contract_address = "0xYourDeployedContractAddress"

# Set up the contract
contract = w3.eth.contract(address=contract_address, abi=abi)

# Use a default account (index 0 from Ganache) — for testing only
default_account = w3.eth.accounts[0]

def hash_dad(dad_text):
    return hashlib.sha256(dad_text.encode()).hexdigest()

def submit_to_blockchain(dad_text):
    dad_hash = hash_dad(dad_text)
    tx_hash = contract.functions.submitDAD(dad_hash).transact({'from': default_account})
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return receipt
