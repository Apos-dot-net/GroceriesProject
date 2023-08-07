from flask_wtf.file import FileAllowed, FileField
from wtforms import Form, StringField, IntegerField, TextAreaField, validators, FloatField


class AddProducts(Form):
    name = StringField("Name", [validators.DataRequired()])
    price = FloatField("Price: ", [validators.DataRequired(), validators.NumberRange(min=0)])
    stock = IntegerField("Stock", [validators.DataRequired(), validators.NumberRange(min=0)])
    desc = TextAreaField("Description", [validators.DataRequired()])

    image_1 = FileField('Image 1', validators=[FileAllowed(['jpg, jpeg, png, svg, gif'])])
