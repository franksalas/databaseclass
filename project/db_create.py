# project/db_create.py


import sqlite3
from _config import DATABASE_PATH

with sqlite3.connect(DATABASE_PATH) as connection:

	# get a cursor object used to execute sql commands
	c = connection.cursor()

	# create the table
	c.execute("""CREATE TABLE Products(
			product_id INTEGER PRIMARY KEY AUTOINCREMENT,
			donor_Id TEXT NOT NULL,
			product_Code TEXT NOT NULL,
			blood_Group TEXT NOT NULL,
			exp_Date TEXT NOT NULL,
			product_Vol INTEGER NOT NULL
			)""")

	# insert dummy data into table
	c.execute(
		'INSERT INTO Products (donor_Id, product_Code, blood_Group, exp_Date, product_Vol)'
		'VALUES("W044615330058","E3077V00","AB","05/10/15", 200)'
		)
	c.execute(
		'INSERT INTO Products (donor_Id, product_Code, blood_Group, exp_Date, product_Vol)'
		'VALUES("W044615192058","E3054V00","A","05/14/15", 120)'
		)
