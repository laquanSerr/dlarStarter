# app/models/company.py

from app.extensions import db

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    contact_info = db.Column(db.String(200))
    services = db.relationship("CompanyServices", backref="company", lazy=True)
    users = db.relationship("Users", backref="company", lazy=True)

    def __repr__(self):
        return f"<Company {self.name}>"