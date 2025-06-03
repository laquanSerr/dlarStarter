import json
import os



DATA_PATH = "contracts/saved_dads.json"

def load_contracts():
    # Load contract data from JSON file
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r") as f:
            return json.load(f)
    return []
def save_contracts(contracts):
    with open(DATA_PATH, "w") as f:
        json.dump(contracts, f, indent=2)

def add_contract(dad_text):
    #Add a new contract to the list
    contracts = load_contracts()
    record = {"dad": dad_text, "status": "submitted"}
    contracts.append(record)
    save_contracts(contracts)

def complete_contract(index):
    #Mark a contract as completed
    contracts = load_contracts()
    if 0 <= index < len(contracts):
        contracts[index]["status"] = "completed"
        save_contracts(contracts)
def validate_contract(dad_text):
    errors = []
    if len(dad_text.strip()) < 20:
        errors.append("Contract is too short.")
    if "DLAR" not in dad_text:
        errors.append("Contract must mention DLAR tokens.")
    if not any(month in dad_text for month in [
        "January", "February", "March", "April", "May", "June", "July", "August",
        "September", "October", "November", "December"
    ]):
        errors.append("Contract must include a delivery of deadline date.")
    return errors
