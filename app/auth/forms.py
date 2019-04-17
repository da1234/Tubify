from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min=0,max=36)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=4,max=4)])
    password_again = PasswordField('Password Again', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min=0,max=36)])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=4,max=4)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')
