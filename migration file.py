import json
import os
import uuid

OLD_PATH = "contracts/saved_dads.json"
NEW_FOLDER = "artifacts/contracts"

if not os.path.exists(NEW_FOLDER):
    os.makedirs(NEW_FOLDER)

if os.path.exists(OLD_PATH):
    with open(OLD_PATH, "r") as f:
        old_contracts = json.load(f)

    for contract in old_contracts:
        contract_id = str(uuid.uuid4())
        contract["id"] = contract_id
        filename = os.path.join(NEW_FOLDER, f"{contract_id}.json")
        with open(filename, "w") as out:
            json.dump(contract, out, indent=2)

    print(f"Migrated {len(old_contracts)} contracts to {NEW_FOLDER}")
else:
    print("No saved_dads.json found to migrate.")
