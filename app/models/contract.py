from app.extensions import db

class Contract(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    initiator_id = db.Column(db.String, nullable=False)
    recipient_id = db.Column(db.String, nullable=False)
    service = db.Column(db.String, nullable=True)
    amount = db.Column(db.Float, nullable=True)
    terms = db.Column(db.Text, nullable=True)
    status = db.Column(db.String, default="pending")
