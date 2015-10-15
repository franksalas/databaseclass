# project/forms.py


from flask_wtf import Form
from wtforms import StringField, DateField, IntegerField, \
    SelectField
from wtforms.validators import DataRequired


class AddProductForm(Form):
    product_id = IntegerField()
    donor_Id = StringField('Donor Id', validators=[DataRequired()])
    product_Code = StringField('Product Code', validators=[DataRequired()])
    blood_Group = StringField('Blood Group', validators=[DataRequired()])
    exp_Date = StringField('Exp Date', validators=[DataRequired()])
    product_Vol = IntegerField('Vol', validators=[DataRequired()])
    status = IntegerField('Status')
