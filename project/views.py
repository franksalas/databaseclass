# project/views.py



from functools import wraps
from flask import Flask, flash, redirect, render_template, \
    request, session, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from forms import AddProductForm, RegisterForm, LoginForm
from sqlalchemy.exc import IntegrityError

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


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text, error), 'error')


def open_products():
    return db.session.query(Product).filter_by(status='1')


def closed_products():
    return db.session.query(Product).filter_by(status='0')

# route handlers


@app.route('/logout/')
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
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
                session['user_id'] = user.id
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
            try:
                db.session.add(new_user)
                db.session.commit()
                flash('Thanks for registering. Please login.')
                return redirect(url_for('login'))
            except IntegrityError:
                error = 'That username and/or email already exist.'
                return render_template('register.html', form=form, error=error)
    return render_template('register.html', form=form, error=error)


@app.route('/products/')
@login_required
def products():
    return render_template(
        'products.html',
        form=AddProductForm(request.form),
        open_products=open_products(),
        closed_products=closed_products()
    )


@app.route('/add/', methods=['GET', 'POST'])
@login_required
def new_product():
    error = None
    form = AddProductForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_product = Product(
                form.donor_Id.data,
                form.product_Code.data,
                form.blood_Group.data,
                form.exp_Date.data,
                form.product_Vol.data,
                '1',
                session['user_id']
            )
            db.session.add(new_product)
            db.session.commit()
            flash('New entry was successfully posted. Thanks.')
            return redirect(url_for('products'))
        else:
            flash('All fields are required')
            return redirect(url_for('products'))
            return render_template(
                'products.html',
                form=form,
                error=error,
                open_products=open_products(),
                closed_products=closed_products
                 )


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
    db.session.query(Product).filter_by(product_id=new_id).delete()
    db.session.commit()
    flash('The product was deleted.')
    return redirect(url_for('products'))


# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
