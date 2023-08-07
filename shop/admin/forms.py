from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, SelectField, IntegerField


class RegistrationForm(FlaskForm):
    name = StringField("Name", [validators.Length(min=3, max=40)])
    username = StringField("Username", [validators.Length(min=4, max=25)])
    email = StringField("Email", [validators.Length(min=6, max=64), validators.Email()])
    password = PasswordField("New Password", [
        validators.DataRequired(),
        validators.EqualTo('confirm', message="Passwords must match")
    ])
    confirm = PasswordField("Repeat Password")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[validators.DataRequired(), validators.Email()])
    password = PasswordField("Password", validators=[validators.DataRequired()])


class ReplenishStockForm(FlaskForm):
    product = SelectField('Product', validators=[validators.DataRequired()], coerce=int)
    category = SelectField('Category', validators=[validators.DataRequired()], coerce=int)
    quantity = IntegerField('Quantity', validators=[validators.DataRequired(), validators.NumberRange(min=1)])
