import json
import os

DATA_PATH = "contracts/saved_dads.json"


def load_contracts():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r") as f:
            return json.load(f)
    return []


def save_contracts(contracts):
    with open(DATA_PATH, "w") as f:
        json.dump(contracts, f, indent=2)


def validate_contract(dad_text):
    if not dad_text or len(dad_text.strip()) == 0:
        raise ValueError("Contract terms cannot be empty.")
    if len(dad_text) > 5000:
        raise ValueError("Contract terms exceed maximum allowed length.")
    # Add more validation rules as needed


def add_contract(dad_text):
    validate_contract(dad_text)
    contracts = load_contracts()

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
