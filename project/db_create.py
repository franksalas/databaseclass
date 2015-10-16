# project/db_create.py
from views import db
from models import Product
# from datetime import date


# create the database and the db table
db.create_all()

# insert data
db.session.add(Product("W044615330058", "E3077V00", "AB", "05/10/15", 200, 1))
db.session.add(Product("W044615192058", "E3054V00", "A", "05/14/15", 120, 1))

# commit the changes
db.session.commit()
