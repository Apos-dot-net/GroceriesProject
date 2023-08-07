from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class PurchaseTrackingForm(FlaskForm):
    # Assuming you have a list of products and categories to populate the SelectField choices
    product = SelectField('Product', validators=[DataRequired()], coerce=int)
    category = SelectField('Category', validators=[DataRequired()], coerce=int)
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Track Purchase')
