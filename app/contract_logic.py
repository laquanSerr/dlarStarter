import json
import os
import uuid

DATA_PATH = "contracts/saved_dads.json"

CONTRACTS_FOLDER = "artifacts/contracts"

def get_contracts():
    contracts = []
    if not os.path.exists(CONTRACTS_FOLDER):
        os.makedirs(CONTRACTS_FOLDER)

    for filename in os.listdir(CONTRACTS_FOLDER):
        if filename.endswith(".json"):
            filepath = os.path.join(CONTRACTS_FOLDER, filename)
            with open(filepath, "r") as f:
                contract = json.load(f)
                contract["id"] = filename.replace(".json", "")
                contracts.append(contract)
    return contracts

def create_contract(data):
    contract_id = str(uuid.uuid4())
    contract = {
        "id": contract_id,
        "created_by": data.get("created_by", "PartyA"),
        "for_party" : data.get("for_party", "PartyB"),
        "terms": data.get("terms", ""),
        "status": "draft"
    }
    return contract_id, contract

def load_contracts():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r") as f:
            return json.load(f)
    return []


def save_contracts(contracts):
    with open(DATA_PATH, "w") as f:
        json.dump(contracts, f, indent=2)


def validate_contract(dad_text):
    if not isinstance(dad_text, str):
        raise TypeError("Contract text must be a string")
    if not dad_text or len(dad_text.strip()) == 0:
        raise ValueError("Contract terms cannot be empty.")
    if len(dad_text) > 5000:
        raise ValueError("Contract terms exceed maximum allowed length.")
    # Add more validation rules as needed


def add_contract(dad_text):
    dad_text = data.get("dad_text", "")
    validate_contract(dad_text)
    contracts = load_contracts()

    contract= {
        "dad_text": dad_text,
        "status": "draft",
        "created_by": data.get("create_by", "PartyA"),
        "for_party":data.get("for_party", "PartyB"),
        "approved_by_party_a": False,
        "approved_by_party_b": False,
    }
    contract_id = str(uuid.uuid4())
    save_contracts(contract_id, contract)

    return contract_id, contract

    # Optional: Check for duplicates
    for c in contracts:
        if c.get("dad") == dad_text:
            raise ValueError("This contract already exists.")

    record = {"dad": dad_text, "status": "submitted"}
    contracts.append(record)
    save_contracts(contracts)


def complete_contract(index):
    contracts = load_contracts()
    if index < 0 or index >= len(contracts):
        raise IndexError("Contract index out of range.")
    if contracts[index]["status"] == "completed":
        raise ValueError("Contract is already completed.")
    contracts[index]["status"] = "completed"
    save_contracts(contracts)
