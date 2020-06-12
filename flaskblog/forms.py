from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User, Admin, Movie, Seat, Screening, Reserved


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    #remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    



class AddShowForm(FlaskForm):
    showtime=StringField('Show Time')
    moviename=StringField('Movie')
    submit = SubmitField('Add')

class DeleteShowForm(FlaskForm):
    showtime=StringField('Show Time')    
    submit = SubmitField('Delete')

class UpdateShowForm(FlaskForm):
    showtime=StringField('Show Time')
    moviename=StringField('Movie')
    submit = SubmitField('Update')

class DeleteMovieForm(FlaskForm):
    moviename=StringField('Movie')
    submit = SubmitField('Delete')

class AddMovieForm(FlaskForm):
    moviename=StringField('Movie')
    year=IntegerField('Year of Release')
    submit = SubmitField('Add')