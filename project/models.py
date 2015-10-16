# project/models.py


from views import db
# import datetime


class Product(db.Model):

    __tablename__ = "products"

    product_id = db.Column(db.Integer, primary_key=True)
    donor_Id = db.Column(db.String, nullable=False)
    product_Code = db.Column(db.String, nullable=False)
    blood_Group = db.Column(db.String, nullable=False)
    exp_Date = db.Column(db.Integer, nullable=False)
    product_Vol = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, donor_Id, product_Code, blood_Group, exp_Date, product_Vol, status, user_id):
        self.donor_Id = donor_Id
        self.product_Code = product_Code
        self.blood_Group = blood_Group
        self.exp_Date = exp_Date
        self.product_Vol = product_Vol
        self.status = status
        self.user_id = user_id

    def __repr__(self):
        return '<name {0}>'.format(self.name)


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    products = db.relationship('Product', backref='poster')

    def __init__(self, name=None, email=None, password=None):
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User {0}>'.format(self.name)
