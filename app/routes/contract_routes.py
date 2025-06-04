from flask import Blueprint, render_template, request, session, redirect
from app.contract_logic import add_contract, get_contracts

contract_bp = Blueprint('contract', __name__)

@contract_bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        data = {
            "dad_text": request.form.get("dad_text"),
            "created_by": session.get("role"),
            "for_party": "PartyB" if session.get("role") == "PartyA" else "PartyA"
        }
        add_contract(data)
        return redirect('/contracts')
    return render_template('create_contract.html')

@contract_bp.route('/contracts')
def contracts():
    role = session.get("role")
    contracts = get_contracts()
    filtered = [c for c in contracts if c["created_by"] == role or c["for_party"] == role]
    return render_template('contracts.html', contracts=filtered, role=role)
