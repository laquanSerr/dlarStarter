from flask import Blueprint, render_template, request, redirect, url_for, session
from app.logic.contract_logic import (
    create_contract,
    get_contracts,
    validate_contract,
    add_contract,
    complete_contract,


)


import uuid

contracts_blueprint = Blueprint("contracts", __name__)

@contracts_blueprint.route('/dashboard')
def dashboard():
    role = session.get('role')
    # Replace this with however you’re tracking the user — example below uses session
    current_user_email = session.get("user_email", "anonymous_user")
    contracts = get_contracts(current_user_email)

    view_contracts = [
        c for c in contracts if c.get("created_by") == role
    ] if role in ["PartyA", "PartyB"] else []

    return render_template("dashboard.html", role=role, contracts=view_contracts)


@contracts_blueprint.route("/", methods=["GET"])
def index():
    role = session.get("role")
    user_id = session.get("user_id", "user@example.com")  # fallback for testing

    all_contracts = get_contracts(user_id)  # Pull all visible contracts (you may adjust this)

    # Filter contracts by role
    if role == "PartyA":
        filtered_contracts = [c for c in all_contracts if c.get("created_by") == user_id]
    elif role == "PartyB":
        filtered_contracts = [c for c in all_contracts if c.get("for_party") == user_id]
    else:
        filtered_contracts = []

    return render_template("index.html", role=role, contracts=filtered_contracts)

@contracts_blueprint.route("/select_role", methods=["POST"])
def select_role():
    selected_role = request.form.get("role")
    session["role"] = selected_role
    session["user_id"] = "user@example.com"  # For now
    return redirect(url_for("contracts.index"))

@contracts_blueprint.route("/create", methods=["POST"])
def create():
    form_data = {
        "initiator_id": session.get("user_id", "user@example.com"),
        "for_party": request.form.get("for_party", "PartyB"),
        "terms": request.form.get("terms", "Default Terms")
    }
    create_contract(form_data)
    return redirect(url_for("contracts.index"))


@contracts_blueprint.route("/approve/<contract_id>", methods=["POST"])
def approve(contract_id):
    contracts = load_contracts() or []
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

@contracts_blueprint.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("contracts.index"))
