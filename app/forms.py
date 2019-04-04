from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class ColForm(FlaskForm):
    start_val = StringField('start_val', validators=[DataRequired()])
    end_val = StringField('end_val', validators=[DataRequired()])
    submit = SubmitField('submit')

class RCForm(FlaskForm):
    start_row = StringField('start_row', validators=[DataRequired()])
    end_row = StringField('end_row', validators=[DataRequired()])
    start_col = StringField('start_col', validators=[DataRequired()])
    end_col = StringField('end_col', validators=[DataRequired()])
    submit = SubmitField('submit')

class DForm(FlaskForm):
    col = StringField('col', validators=[DataRequired()])
    bot = StringField('bot', validators=[DataRequired()])
    top = StringField('top', validators=[DataRequired()])
    submit = SubmitField('submit')

class PlotForm(FlaskForm):
    col_1 = StringField('col_1', validators=[DataRequired()])
    #col_2 = StringField('col_2', validators=[DataRequired()])
    submit = SubmitField('submit')

class UploadForm(FlaskForm):
    file = FileField(validators=[FileRequired()])
    submit = SubmitField('submit')

