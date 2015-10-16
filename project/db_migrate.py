# project/db_migrate.py


from views import db
from _config import DATABASE_PATH

import sqlite3
from datetime import datetime

with sqlite3.connect(DATABASE_PATH) as connection:

    # get a cursor object used to execute SQL commands
    c = connection.cursor()

    # temporarily change the name of tasks table
    c.execute("""ALTER TABLE products RENAME TO old_products""")

    # recreate a new tasks table with updated schema
    db.create_all()

    # retrieve data from old_tasks table
    c.execute("""SELECT donor_Id, product_Code, blood_Group, exp_Date,
                product_vol, status FROM old_products ORDER BY product_id ASC""")

    # save all rows as a list of tuples; set posted_date to now and user_id to 1
    data = [(row[0], row[1], row[2], row[3], row[4], row[5], 1) for row in c.fetchall()]

    # insert data to tasks table
    c.executemany("""INSERT INTO products (donor_Id, product_Code, blood_Group, exp_Date,
                product_vol, status, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)""", data)

    # delete old_tasks table
    c.execute("DROP TABLE old_products")
    