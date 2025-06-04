from flask import  Flask, request, jsonify, redirect, render_template, send_from_directory
from app.contract_logic import load_contracts, add_contract, complete_contract, get_contracts

app = Flask(__name__)

DATA_PATH = "contracts/saved_dads.json"

contracts = {}  # Simulating contract storage
@app.route('/contracts')
def list_contracts():
    contracts = get_contracts()
    return render_template('contracts.html', contracts=contracts)

def load_contract(contract_id):
    return contracts.get(contract_id)

def save_contract(contract_id, contract):
    contracts[contract_id] = contract

@app.route('/')
def index():
    from app.contract_logic import get_contracts
    contracts = get_contracts()
    return render_template('index.html', contracts=contracts)

@app.route('/create', methods=['POST'])
def create():
    data = request.form.to_dict()
    contract_id, contract = add_contract(data)
    contracts[contract_id] = contract
    return jsonify({'status': 'created', 'contract_id': contract_id})

@app.route('/edit/<contract_id>', methods=['POST'])
def edit(contract_id):
    role = request.form.get("role")
    contract = load_contract(contract_id)  # Unified contract retrieval

    if not contract:
        return jsonify({"error": "Contract not found"}), 404

    # Standardized Authorization Check
    if role != contract.get("for_party"):
        return jsonify({"error": "Unauthorized - Only Party B may edit"}), 403

    # Handling Multiple Editable Fields
    updated_terms = request.form.get("terms")
    new_text = request.form.get("dad_text")

    if updated_terms:
        contract["terms"] = updated_terms  # Updating contract terms
    if new_text:
        contract["dad_text"] = new_text  # Updating dad_text

    save_contract(contract_id, contract)  # Unified saving method

    return jsonify({'status': 'edited', 'contract_id': contract_id})


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

    contract["status"] = "approved"
    contract["approved_by_party_a"] = True

    save_contract(contract_id, contract)

    return redirect(f"/summary/{contract_id}")

@app.route('/contracts', methods=['GET'])
def get_contracts():
    return jsonify(load_contracts())

@app.route('/submit', methods=['POST'])
def submit_contract():
    data = request.get_json()
    if not data or "dad" not in data:
        return jsonify({"message": "Invalid request format."}), 400

    try:
        add_contract(data["dad"])
        return jsonify({"message": "Contract submitted successfully."}), 200
    except ValueError as ve:
        return jsonify({"message": str(ve)}), 400
    except Exception as e:
        return jsonify({"message": "Unexpected error: " + str(e)}), 500

@app.route('/complete', methods=['POST'])
def mark_complete():
    data = request.get_json()
    try:
        complete_contract(data['index'])
        return jsonify({"message": "Contract marked as completed."}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)







