from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=True)
    password = db.Column(db.String(16))
    mail = db.Column(db.String(50))
    tel = db.Column(db.String(16))
    school = db.Column(db.String(50))
    img = db.Column(db.String(50))
    address = db.Column(db.Text)
    is_admin = db.Column(db.Boolean)
    is_ban = db.Column(db.Boolean)

    gives = db.relationship('Give', backref='user', lazy='dynamic')
    gets = db.relationship('Get', backref='user', lazy='dynamic')

    def is_authenticated(self):
        return True

    def is_active(self):
        return not self.is_ban

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    category = db.Column(db.String(10))
    img = db.Column(db.String(50))
    press = db.Column(db.String(50))
    author = db.Column(db.String(50))
    note = db.Column(db.Text)
    status = db.Column(db.Boolean)
    num = db.Column(db.Integer)

    gives = db.relationship('Give', backref='book', lazy='dynamic')
    gets = db.relationship('Get', backref='book', lazy='dynamic')



class Give(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    author = db.Column(db.Integer, db.ForeignKey('user.id'))
    time = db.Column(db.DateTime)
    status = db.Column(db.Integer)

class Get(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    author = db.Column(db.Integer, db.ForeignKey('user.id'))
    time = db.Column(db.DateTime)
    status = db.Column(db.Integer)
