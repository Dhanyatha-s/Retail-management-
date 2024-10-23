from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, FloatField, DecimalField
from wtforms.validators import DataRequired, ValidationError

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])  # Add this line to require email
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Signup')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class AddProductForm(FlaskForm):
    
    name = StringField('Product Name', validators=[DataRequired()])
    category = SelectField('Category', 
        choices=[('solid', 'Solid Item'), ('liquid', 'Liquid Item')],validators=[DataRequired()]
    )
    price = DecimalField('Price per Unit', validators=[DataRequired()])
    unit = SelectField('Unit', choices=[('kg', 'Kilogram'), ('liter', 'Liter')], validators=[DataRequired()])
    submit = SubmitField('Add Product')
   