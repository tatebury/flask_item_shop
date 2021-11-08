from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired


class ItemCreationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    img = StringField('Image Link')
    description = StringField('Description')
    submit = SubmitField('Create Item')
    
class ItemEditingForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    img = StringField('Image Link')
    description = StringField('Description')
    submit = SubmitField('Submit Edit')