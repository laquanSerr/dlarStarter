from flask import Flask, render_template, request, redirect, jsonify, send_from_directory
from dlarStarter.app.logic.contract_logic import add_contract, load_contract, get_contracts, complete_contract, validate_contract, approve_contract, save_contract, create_contract  # Ensure these functions are defined in contract_logic.py
from app.routes.dashboard_routes import dashboard_blueprint
from app import create_app
from enum import Enum







#DATA_PATH = "contracts/saved_dads.json"




app = create_app()



class ContractStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EDITED = "edited"
class UserRole(Enum):
    PARTY_A = "party_a"
    PARTY_B = "party_b"

@app.route("/contracts/json")
def contracts():
    all_contracts = get_contracts()
    return jsonify(all_contracts)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    user = authenticate_user(email, password)
    if user:
        next_page = request.args.get("next") or "/dashboard"
        return redirect(next_page)
    return jsonify({"error": "Invalid credentials"}), 401


@app.route('/contract', methods=['POST'])
def handle_contract():
    data = request.get_json()

    if not data or ("dad" not in data and "contract" not in data):
        return jsonify({"message": "Invalid request format."}), 400

    try:
        contract_data = data.get("dad") or data.get("contract")
        contract_id, contract = add_contract(contract_data)
        return jsonify({"contract_id": contract_id, "contract": contract}), 201
    except ValueError as ve:
        return jsonify({"message": str(ve)}), 400
    except Exception as e:
        return jsonify({"message": "Unexpected error: " + str(e)}), 500

"""@app.route('/contracts')
def list_contracts():
    contracts = get_contracts()
    return render_template('contracts.html', contracts=contracts)"""




@app.route('/edit/<contract_id>', methods=['POST'])
def edit(contract_id):
    role = request.form.get("role")
    contract = load_contract(contract_id)  # Unified contract retrieval

    if not contract:
        return jsonify({"error": "Contract not found"}), 404

    # Standardized Authorization Check using Enum
    if role != contract.get("for_party"):
        return jsonify({"error": "Unauthorized - Only Party B may edit"}), 403

    # Handling Multiple Editable Fields
    updated_terms = request.form.get("terms")
    new_text = request.form.get("dad_text")

    if updated_terms:
        contract["terms"] = updated_terms  # Updating contract terms
    if new_text:
        contract["dad_text"] = new_text  # Updating dad_text

    # Updating contract status using Enum
    contract["status"] = ContractStatus.EDITED.value

    save_contract(contract_id, contract)  # Unified saving method

    return jsonify({'status': ContractStatus.EDITED.value, 'contract_id': contract_id})


@app.route('/summary/<contract_id>', methods=['GET'])
def summary(contract_id):
    contract = load_contract(contract_id)

    created_by = contract.get("created_by", "PartyA")
    for_party = contract.get("for_party", "PartyB")
    status = contract.get("status", "draft")
    approved_by_party_a = contract.get("approved_by_party_a", False)

    return render_template(
        "summary.html",
        contract_id=contract_id,
        dad_text=contract.get("dad_text", ""),
        created_by=created_by,
        for_party=for_party,
        status=status,
        approved_by_party_a=approved_by_party_a
    )


@app.route('/approve/<contract_id>', methods=['POST'])



def approve(contract_id):
    role = request.form.get("role")
    contract = load_contract(contract_id)

    if not contract:
        return jsonify({"error": "Contract not found"}), 404

    if role != contract.get("created_by"):
        return jsonify({"error": "Unauthorized - Only Party A may approve"}), 403

    contract["status"] = ContractStatus.APPROVED.value
    contract["approved_by_party_a"] = True

    save_contract(contract_id, contract)

    return redirect(f"/summary/{contract_id}")



@app.route("/complete/<contract_id>", methods=["POST"])
def mark_contract_complete(contract_id):
    try:
        complete_contract(contract_id)
        return jsonify({"message": f"Contract {contract_id} marked as completed."}), 200
    except FileNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Unexpected error occurred."}), 500

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('app/static', filename)


if __name__ == "__main__":
    app.run(debug=True)







