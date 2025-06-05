from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Contract

dashboard_blueprint = Blueprint("dashboard", __name__)

@dashboard_blueprint.route("/dashboard")
@login_required
def dashboard():
    sent_contracts = Contract.query.filter_by(sender_id=current_user.id).all()
    received_contracts = Contract.query.filter_by(receiver_id=current_user.id).all()
    return render_template('dashboard.html',
                           sent_contracts=sent_contracts,
                           received_contracts=received_contracts)



@dashboard_blueprint.route("/dashboard")
@login_required
def dashboard_view():
    user_id = current_user.id
    sent_contracts = Contract.query.filter_by(initiator_id=user_id).all()
    received_contracts = Contract.query.filter_by(recipient_id=user_id).all()
    return render_template("dashboard.html", sent=sent_contracts, received=received_contracts)

