from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DateField, IntegerField, ValidationError
from wtforms.validators import DataRequired, EqualTo, InputRequired, Optional

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class AuthForm(FlaskForm):
    submit = SubmitField('Authorize Spotify')

class SubmissionForm(FlaskForm):
    mbid = StringField('MBID', validators=[InputRequired()])
    name = StringField('Playlist Name', validators=[InputRequired()])
    
    platform = SelectField(
    'Platform',
    choices= [('Spotify','Spotify'),('Apple Music','Apple Music')],
    #value, displayed label
    #validators=[DataRequired()],
    default='Spotify'
    )

    # def req_spotify(FlaskForm, platform):
    #     if platform.data!='Spotify1':
    #         raise ValidationError('We currently only support Spotify')
    max_songs = IntegerField('Max Songs', default=15)
    num_concerts = IntegerField('Number of recent concerts to consider', default=5)
    date = DateField('Start Date', format='%d/%m/%Y', validators=[Optional()])
    submit = SubmitField('Generate Playlist')