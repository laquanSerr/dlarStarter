from flask import  Flask, request, jsonify, render_template, send_from_directory
from app.contract_logic import load_contracts, add_contract, complete_contract

app = Flask(__name__)

DATA_PATH = "contracts/saved_dads.json"

@app.route('/')
def index():
    return render_template('index.html')

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







