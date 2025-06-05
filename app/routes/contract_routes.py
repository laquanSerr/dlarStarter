from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app.models import db, Contract, Company

contracts_blueprint = Blueprint("contracts", __name__)

@contracts_blueprint.route("/create", methods=["GET", "POST"])
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
