# project/views.py



from functools import wraps
from flask import Flask, flash, redirect, render_template, \
    request, session, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from forms import AddProductForm, RegisterForm, LoginForm


# config

app = Flask(__name__)
app.config.from_object('_config')
db = SQLAlchemy(app)

from models import Product, User


# helper functions


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
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(name=request.form['name']).first()
            if user is not None and user.password == request.form['password']:
                session['logged_in'] = True
                flash('Welcome!')
                return redirect(url_for('products'))
            else:
                error = 'Invalid username or password.'
        else:
            error = 'Both fields are required.'
    return render_template('login.html', form=form, error=error)


@app.route('/register/', methods=['GET', 'POST'])
def register():
    error = None
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_user = User(
                form.name.data,
                form.email.data,
                form.password.data,
            )
            db.session.add(new_user)
            db.session.commit()
            flash('Thanks for registering. Please login.')
            return redirect(url_for('login'))
    return render_template('register.html', form=form, error=error)


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

