# project/views.py


# import sqlite3
from functools import wraps

from flask import Flask, flash, redirect, render_template, \
    request, session, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from forms import AddProductForm


# config

app = Flask(__name__)
app.config.from_object('_config')
db = SQLAlchemy(app)
from models import Product


# helper functions

# def connect_db():
#     return sqlite3.connect(app.config['DATABASE_PATH'])


def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap


# route handlers

@app.route('/logout/')
def logout():
    session.pop('logged_in', None)
    flash('Goodbye!')
    return redirect(url_for('login'))


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or \
                request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid Credentials. Please try again.'
            return render_template('login.html', error=error)
        else:
            session['logged_in'] = True
            flash('Welcome!')
            return redirect(url_for('products'))
    return render_template('login.html')



# @app.route('/prdoucts/')
# @login_required
# def products():
#     g.db = connect_db()
#     cur = g.db.execute(
#         'select donor_Id, product_Code, blood_Group, exp_Date, product_Vol, product_id from products where status=1'
#     )
#     open_products = [
#         dict(donor_Id=row[0], product_Code=row[1], blood_Group=row[2],
#              exp_Date=row[3], product_Vol=row[4], product_id=row[5]) for row in cur.fetchall()
#     ]
#     cur = g.db.execute(
#         'select donor_Id, product_Code, blood_Group, exp_Date, product_Vol, product_id from products where status=0'
#     )
#     closed_products = [
#         dict(donor_Id=row[0], product_Code=row[1], blood_Group=row[2],
#              exp_Date=row[3], product_Vol=row[4], product_id=row[5]) for row in cur.fetchall()
#     ]
#     g.db.close()
#     return render_template(
#         'products.html',
#         form=AddProductForm(request.form),
#         open_products=open_products,
#         closed_products=closed_products
#     )


@app.route('/products/')
@login_required
def products():
    open_products = db.session.query(Product) \
        .filter_by(status='1').order_by(Product.exp_Date.asc())
    closed_products = db.session.query(Product) \
        .filter_by(status='0').order_by(Product.exp_Date.asc())
    return render_template(
        'products.html',
        form=AddProductForm(request.form),
        open_products=open_products,
        closed_products=closed_products
    )


    # add new product


# @app.route('/add/', methods=['POST'])
# @login_required
# def new_products():
#     g.db = connect_db()
#     donor_Id = request.form['donor_Id']
#     product_Code = request.form['product_Code']
#     blood_Group = request.form['blood_Group']
#     exp_Date = request.form['exp_Date']
#     product_Vol = request.form['product_Vol']
#     if not donor_Id or not product_Code or not blood_Group or not exp_Date or not product_Vol:
#         flash("All fields are required. Please try again.")
#         return redirect(url_for('products'))
#     else:
#         g.db.execute('insert into products (donor_Id, product_Code, blood_Group, exp_Date, product_Vol, status) \
#             values (?, ?, ?, ?, ?, 1)', [
#                 request.form['donor_Id'],
#                 request.form['product_Code'],
#                 request.form['blood_Group'],
#                 request.form['exp_Date'],
#                 request.form['product_Vol']
#             ]
#         )
#         g.db.commit()
#         g.db.close()
#         flash('New entry was successfully posted. Thanks.')
#         return redirect(url_for('products'))


@app.route('/add/', methods=['GET', 'POST'])
@login_required
def new_product():
    form = AddProductForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_product = Product(
                form.donor_Id.data,
                form.product_Code.data,
                form.blood_Group.data,
                form.exp_Date.data,
                form.product_Vol.data,
                '1'
            )
            db.session.add(new_product)
            db.session.commit()
            flash('New entry was successfully posted. Thanks.')
    return redirect(url_for('products'))


# Mark tasks as complete
@app.route('/complete/<int:product_id>/')
@login_required
def complete(product_id):
    new_id = product_id
    db.session.query(Product).filter_by(product_id=new_id).update({"status": "0"})
    db.session.commit()

    flash('The product was marked as complete.')
    return redirect(url_for('products'))


# Delete Tasks
@app.route('/delete/<int:product_id>/')
@login_required
def delete_entry(product_id):
    new_id = product_id
    db.session.query(Product).filter_by(product_id=new_id).deleted
    db.session.commit()
    flash('The product was deleted.')
    return redirect(url_for('products'))

