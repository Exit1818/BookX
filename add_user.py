from app.models import User
from app import db

user = User(username = 'Exit',
			password = '123',
			mail = 'user@user.com',
			tel = '18812345678',
			school = 'BUAA',
			address = 'BUAA',
			is_admin = False,
			is_ban = False)

db.session.add(user)
db.session.commit()