# project/forms.py


from flask_wtf import Form
from wtforms import StringField, IntegerField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo


class RegisterForm(Form):
    name = StringField(
        'Username',
        validators=[DataRequired(), Length(min=6, max=25)]
    )
    email = StringField(
        'Email',
        validators=[DataRequired(), Length(min=6, max=40)]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=6, max=40)])
    confirm = PasswordField(
        'Repeat Password',
        validators=[DataRequired(), EqualTo('password', message='Passwords must match')]
    )


class LoginForm(Form):
    name = StringField(
        'Username',
        validators=[DataRequired()]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired()]
    )


class AddProductForm(Form):
    product_id = IntegerField()
    donor_Id = StringField('Donor Id', validators=[DataRequired()])
    product_Code = StringField('Product Code', validators=[DataRequired()])
    blood_Group = StringField('Blood Group', validators=[DataRequired()])
    exp_Date = StringField('Exp Date', validators=[DataRequired()])
    product_Vol = IntegerField('Vol', validators=[DataRequired()])
    status = IntegerField('Status')
