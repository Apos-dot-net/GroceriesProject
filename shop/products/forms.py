from flask_wtf.file import FileAllowed, FileField
from wtforms import Form, StringField, IntegerField, TextAreaField, validators


class AddProducts(Form):
    name = StringField("Name", [validators.DataRequired()])
    price = IntegerField("Price: ", [validators.DataRequired()])
    stock = IntegerField("Stock", [validators.DataRequired()])
    desc = TextAreaField("Description", [validators.DataRequired()])

    image_1 = FileField('Image 1', validators=[FileAllowed(['jpg, jpeg, png, svg, gif'])])
