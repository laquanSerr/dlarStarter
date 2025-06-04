import json
import os
import uuid

# Directory for individual contract files
CONTRACTS_FOLDER = "artifacts/contracts"

# Ensure the directory exists
if not os.path.exists(CONTRACTS_FOLDER):
    os.makedirs(CONTRACTS_FOLDER)

# -------------------------------
# Function: Get all saved contracts
# -------------------------------
def get_contracts():
    contracts = []
    for filename in os.listdir(CONTRACTS_FOLDER):
        if filename.endswith(".json"):
            filepath = os.path.join(CONTRACTS_FOLDER, filename)
            with open(filepath, "r") as f:
                contract = json.load(f)
                contract["id"] = filename.replace(".json", "")
                contracts.append(contract)
    return contracts

# -------------------------------
# Function: Validate contract text
# -------------------------------
def validate_contract(dad_text):
    if not isinstance(dad_text, str):
        raise TypeError("Contract text must be a string.")
    if not dad_text.strip():
        raise ValueError("Contract terms cannot be empty.")
    if len(dad_text) > 5000:
        raise ValueError("Contract terms exceed maximum allowed length.")

# -------------------------------
# Function: Add new contract
# -------------------------------
def add_contract(data):
    dad_text = data.get("dad_text", "")
    validate_contract(dad_text)

    contract_id = str(uuid.uuid4())
    contract = {
        "id": contract_id,
        "dad_text": dad_text,
        "status": "draft",
        "created_by": data.get("created_by", "PartyA"),
        "for_party": data.get("for_party", "PartyB"),
        "approved_by_party_a": False,
        "approved_by_party_b": False,
    }

    filename = os.path.join(CONTRACTS_FOLDER, f"{contract_id}.json")
    with open(filename, "w") as f:
        json.dump(contract, f, indent=2)

    return contract_id, contract

# -------------------------------
# Function: Mark a contract as completed
# -------------------------------
def complete_contract(contract_id):
    filepath = os.path.join(CONTRACTS_FOLDER, f"{contract_id}.json")
    if not os.path.exists(filepath):
        raise FileNotFoundError("Contract not found.")

    with open(filepath, "r") as f:
        contract = json.load(f)

    if contract["status"] == "completed":
        raise ValueError("Contract is already completed.")

    contract["status"] = "completed"

    with open(filepath, "w") as f:
        json.dump(contract, f, indent=2)
