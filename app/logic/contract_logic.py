import json
import os
import uuid
import logging

# Directory for individual contract files
CONTRACTS_FOLDER = "artifacts/contracts"



logging.basicConfig(
    filename="contract_logs.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def create_contract(data):
    if not os.path.exists(CONTRACTS_FOLDER):
        os.makedirs(CONTRACTS_FOLDER)

    contract_id = str(uuid.uuid4())
    contract = {
        "id": contract_id,
        "initiator_id": data.get("initiator_id", "user@example.com"),
        "for_party": data.get("for_party", "PartyB"),
        "terms": data.get("terms", ""),
        "status": "draft"
    }

    filepath = os.path.join(CONTRACTS_FOLDER, f"{contract_id}.json")
    with open(filepath, "w") as f:
        json.dump(contract, f, indent=2)

    return contract

# -------------------------------
# Function: Get all saved contracts
# -------------------------------
def get_contracts(current_user_email):
    contracts = []
    if not os.path.exists(CONTRACTS_FOLDER):
        os.makedirs(CONTRACTS_FOLDER)

    for filename in os.listdir(CONTRACTS_FOLDER):
        if filename.endswith(".json"):
            filepath = os.path.join(CONTRACTS_FOLDER, filename)
            with open(filepath, "r") as f:
                contract = json.load(f)
                contract["id"] = filename.replace(".json", "")

                # Only include contracts involving the current user
                if (contract.get("initiator_id") == current_user_email or
                        contract.get("recipient_email") == current_user_email):
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

    contract = {
        "id": str(uuid.uuid4()),
        "initiator_id": current_user.id,
        "recipient_email": data.get("recipient_email", ""),  # or recipient_id
        "terms": data.get("terms", ""),
        "status": "draft",
        "approved_by_initiator": False,
        "approved_by_recipient": False,
        "created_at": datetime.utcnow().isoformat()
    }
    return contract_id, contract

    contract_id = str(uuid.uuid4())
    file_path = os.path.join(CONTRACTS_FOLDER, f"{contract_id}.json")
    with open(file_path, "w") as f:
        json.dump(contract, f, indent=2)

    logger.info(f"Contract {contract_id} created by {contract['created_by']}")

    return contract_id, contract


def save_contract(contract_id, contract):
    filename = f"{contract_id}.json"
    filepath = os.path.join(CONTRACTS_FOLDER, filename)
    with open(filepath, "w") as f:
        json.dump(contract, f, indent=2)


def approve_contract(contract_id, user):
    filepath = os.path.join(CONTRACTS_FOLDER, f"{contract_id}.json")
    if not os.path.exists(filepath):
        logger.warning(f"Attempted approval: Contract {contract_id} not found.")
        raise FileNotFoundError("Contract not found.")

    with open(filepath, "r") as f:
        contract = json.load(f)

    if user == "PartyA":
        contract["approved_by_party_a"] = True
    elif user == "PartyB":
        contract["approved_by_party_b"] = True
    else:
        logger.error(f"Invalid approval attempt by {user} for {contract_id}")
        raise ValueError("Invalid user role.")

    with open(filepath, "w") as f:
        json.dump(contract, f, indent=2)

    logger.info(f"Contract {contract_id} approved by {user}")

    return contract


# -------------------------------
# Function: Mark a contract as completed
# -------------------------------
def complete_contract(contract_id):
    filepath = os.path.join(CONTRACTS_FOLDER, f"{contract_id}.json")
    if not os.path.exists(filepath):
        logger.warning(f"Completion attempt: Contract {contract_id} not found.")
        raise FileNotFoundError("Contract not found.")

    with open(filepath, "r") as f:
        contract = json.load(f)

    if contract["status"] == "completed":
        logger.info(f"Contract {contract_id} already marked as completed.")
        raise ValueError("Contract is already completed.")

    contract["status"] = "completed"

    with open(filepath, "w") as f:
        json.dump(contract, f, indent=2)

    logger.info(f"Contract {contract_id} marked as completed.")

    return contract

