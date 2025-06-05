# app/routes/contract_routes.py
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app.logic.contract_logic import add_contract, get_contracts

contract_blueprint = Blueprint("contracts", __name__)

@contract_blueprint.route("/create", methods=["GET", "POST"])
@login_required
def create_contract():
    companies = Company.query.filter(Company.id != current_user.id).all()
    if request.method == "POST":
        recipient_id = request.form["recipient_id"]
        terms = request.form["terms"]

        contract = Contract(
            initiator_id=current_user.id,
            recipient_id=recipient_id,
            terms=terms,
            amount=1000.00,
            status="pending"
        )
        db.session.add(contract)
        db.session.commit()
        return redirect(url_for("dashboard.dashboard_view"))
    return render_template("create_contract.html", companies=companies)

@contract_blueprint.route("/contracts", methods=["GET"])
@login_required
def contracts():
    user_email = current_user.email
    contracts = get_contracts(user_email)
    return render_template("contracts.html", contracts=contracts)