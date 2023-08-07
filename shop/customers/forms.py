from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, PasswordField, SubmitField, validators, ValidationError

from .models import RegisterModel


def validate_username(username):
    if RegisterModel.query.filter_by(username=username.data).first():
        raise ValidationError("Username already Exists.")


def validate_email(email):
    if RegisterModel.query.filter_by(email=email.data).first():
        raise ValidationError("Email already Exists.")


class CustomerRegistrationForm(FlaskForm):
    name = StringField('Name', [validators.DataRequired()])
    username = StringField('Username', [validators.DataRequired()])
    email = StringField("Email", validators=[validators.Email(), validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired(),
                                          validators.EqualTo('confirm', message="Both passwords should match")])
    confirm = PasswordField("Repeat Password", [validators.DataRequired()])
    country = StringField('Country', [validators.DataRequired()])
    state = StringField('State', [validators.DataRequired()])
    city = StringField('City', [validators.DataRequired()])
    contact = StringField('Contact', [validators.DataRequired()])
    address = StringField('Address', [validators.DataRequired()])

    profile_image = FileField("Profile Image", validators=[FileAllowed(['jpg', 'png', 'jpeg'], "Images only")])

    submit = SubmitField("Register")


class CustomerLoginForm(FlaskForm):
    email = StringField("Email", validators=[validators.Email(), validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])
