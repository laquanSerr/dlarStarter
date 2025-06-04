from flask import Blueprint, session, request, redirect, url_for

auth = Blueprint('auth', __name__)

#We'll allow Party A or Party B to select a role and store it in their session.

@auth.route('/login', methods=['POST'])
def login():
    role = request.form.get("role")
    if request.method == "POST":
        # login logic here
        return redirect(url_for("index"))
    return render_template("login.html")



