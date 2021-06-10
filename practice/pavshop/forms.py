from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError    
from pavshop.models import User


class RegistrationForm(FlaskForm):

    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=4, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    parol = PasswordField('Password', validators=[DataRequired(), Length(min=7, max=22)])
    parol_confirm = PasswordField('Password confirm', validators=[DataRequired(), EqualTo('parol')])
    bio = TextAreaField('Bio')
    image = FileField('Image')
    submit = SubmitField('Resgister')


    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already in our database')

class  LoginForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Email()])
    parol = PasswordField('Password', validators=[DataRequired()])

    submit = SubmitField('Login')


class UserPostForm(FlaskForm):

    title = StringField('Title', validators=[DataRequired(), Length(min=4, max=50)])
    short_description = StringField('Short Description', validators=[DataRequired()])
    content = TextAreaField('Content')
    image = FileField('Image')
    submit = SubmitField('Share')
