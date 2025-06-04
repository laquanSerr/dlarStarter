from flask import Blueprint, render_template, session

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def dashboard():
    role = session.get("role")
    return render_template('dashboard.html', role=role)
