# project/models.py


from views import db


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __init__(self, name=None, email=None, password=None):
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User {0}>'.format(self.name)


class Product(db.Model):

    __tablename__ = "products"

    product_id = db.Column(db.Integer, primary_key=True)
    donor_Id = db.Column(db.String, nullable=False)
    product_Code = db.Column(db.String, nullable=False)
    blood_Group = db.Column(db.String, nullable=False)
    exp_Date = db.Column(db.Integer, nullable=False)
    product_vol = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer)

    def __init__(self, donor_Id, product_Code, blood_Group, exp_Date, product_vol, status):
        self.donor_Id = donor_Id
        self.product_Code = product_Code
        self.blood_Group = blood_Group
        self.exp_Date = exp_Date
        self.product_vol = product_vol
        self.status = status

    def __repr__(self):
        return '<name {0}>'.format(self.name)
