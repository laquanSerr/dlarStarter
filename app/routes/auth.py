from flask import Blueprint, render_template, redirect, request, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from app.models import db, User

auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')

#We'll allow Party A or Party B to select a role and store it in their session.
"""@auth.route('/login', methods=['POST'])
def login():
    role = request.form.get("role")
    if request.method == "POST":
        # login logic here
        return redirect(url_for("index"))
    return render_template("login.html")"""



@auth_blueprint.route("/login", methods=["Get", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("contracts.index"))
        else:
            flash("Invalid login")
    return render_template("login.html")

@auth_blueprint.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered")
            return redirect(url_for("auth.register"))
        new_user = User(
            email=email,
            password=generate_password_hash(password),
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("contracts.index"))
    return render_template("register.html")

@auth_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


