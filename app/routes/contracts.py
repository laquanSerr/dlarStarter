from flask import Blueprint, render_template, request, redirect, url_for, session
from app.logic.contract_logic import (
    get_contracts,
    validate_contract,
    add_contract,
    complete_contract
)
import uuid

bp = Blueprint("contracts", __name__)

@bp.route("/", methods=["GET"])
def index():
    contracts = get_contracts()
    return render_template("index.html", contracts=contracts)

@bp.route("/create", methods=["POST"])
def create():
    data = request.form
    contract_id, contract = create_contract(data)
    # Save to file
    all_contracts = load_contracts()
    all_contracts.append(contract)
    save_contracts(all_contracts)
    return redirect(url_for("contracts.index"))

@bp.route("/approve/<contract_id>", methods=["POST"])
def approve(contract_id):
    contracts = load_contracts()
    for contract in contracts:
        if contract["id"] == contract_id:
            user = request.form.get("user")
            if user == "PartyA":
                contract["approved_by_party_a"] = True
            elif user == "PartyB":
                contract["approved_by_party_b"] = True
            break
    save_contracts(contracts)
    return redirect(url_for("contracts.index"))
