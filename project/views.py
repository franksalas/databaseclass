# project/views.py


import sqlite3
from functools import wraps

from flask import Flask, flash, redirect, render_template, \
    request, session, url_for, g
from forms import AddProductForm


# config

app = Flask(__name__)
app.config.from_object('_config')


# helper functions

def connect_db():
    return sqlite3.connect(app.config['DATABASE_PATH'])


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
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] \
                or request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid Credentials. Please try again.'
            return render_template('login.html', error=error)
        else:
            session['logged_in'] = True
            flash('Welcome!')
            return redirect(url_for('products'))
    return render_template('login.html')


@app.route('/prdoucts/')
@login_required
def products():
    g.db = connect_db()
    cur = g.db.execute(
        'select donor_Id, product_Code, blood_Group, exp_Date, product_Vol, product_id from products where status=1'
    )
    open_products = [
        dict(donor_Id=row[0], product_Code=row[1], blood_Group=row[2],
             exp_Date=row[3], product_Vol=row[4], product_id=row[5]) for row in cur.fetchall()
    ]
    cur = g.db.execute(
        'select donor_Id, product_Code, blood_Group, exp_Date, product_Vol, product_id from products where status=0'
    )
    closed_products = [
        dict(donor_Id=row[0], product_Code=row[1], blood_Group=row[2],
             exp_Date=row[3], product_Vol=row[4], product_id=row[5]) for row in cur.fetchall()
    ]
    g.db.close()
    return render_template(
        'products.html',
        form=AddProductForm(request.form),
        open_products=open_products,
        closed_products=closed_products
    )

    # add new product


@app.route('/add/', methods=['POST'])
@login_required
def new_products():
    g.db = connect_db()
    donor_Id = request.form['donor_Id']
    product_Code = request.form['product_Code']
    blood_Group = request.form['blood_Group']
    exp_Date = request.form['exp_Date']
    product_Vol = request.form['product_Vol']
    if not donor_Id or not product_Code or not blood_Group or not exp_Date or not product_Vol:
        flash("All fields are required. Please try again.")
        return redirect(url_for('products'))
    else:
        g.db.execute('insert into products (donor_Id, product_Code, blood_Group, exp_Date, product_Vol, status) \
            values (?, ?, ?, ?, ?, 1)', [
                request.form['donor_Id'],
                request.form['product_Code'],
                request.form['blood_Group'],
                request.form['exp_Date'],
                request.form['product_Vol']
            ]
        )
        g.db.commit()
        g.db.close()
        flash('New entry was successfully posted. Thanks.')
        return redirect(url_for('products'))


# Mark tasks as complete
@app.route('/complete/<int:product_id>/')
@login_required
def complete(product_id):
    g.db = connect_db()
    g.db.execute(
        'update products set status = 0 where product_id='+str(product_id)
    )
    g.db.commit()
    g.db.close()
    flash('The product was marked as complete.')
    return redirect(url_for('products'))


# Delete Tasks
@app.route('/delete/<int:product_id>/')
@login_required
def delete_entry(product_id):
    g.db = connect_db()
    g.db.execute('delete from products where product_id='+str(product_id))
    g.db.commit()
    g.db.close()
    flash('The product was deleted.')
    return redirect(url_for('products'))


