from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, StringField
from wtforms.validators import InputRequired, email, Length

# form used in checkout
class CheckoutForm(FlaskForm):
    firstname = StringField("First name", validators=[
                            Length(min=1, max=20)])
    surname = StringField("Surname", validators=[
                          Length(min=1, max=20)])
    email = StringField("Email Address", validators=[
        InputRequired(message='Please provide a value'), email(message='Invalid email format'), Length(min=3, max=30)])
    phone = StringField("Phone number", validators=[
                        InputRequired(message='Please provide a value'), Length(min=5, max=13)])
    submit = SubmitField("Submit", render_kw={
                         'style': 'margin-top: 10px; background-color: #FFFFFF; color: #000000; border-color:#000000'})
