from flask import Blueprint, render_template, request, session, redirect

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        role = request.form.get('role')
        session['role'] = role
        return redirect('/dashboard')
    return render_template('login.html')
