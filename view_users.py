from app import create_app
from app.models import db, User

app = create_app()

with app.app_context():
    users = User.query.all()
    for user in users:
        print(f"ID:{user.id}, Email: {user.email}, Name: {user.name}")
