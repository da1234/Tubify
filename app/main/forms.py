from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from app.models import Playlist, Song

class SearchSongForm(FlaskForm):
    # Todo: change songname param
    songname = StringField('Song', validators=[DataRequired(),Length(min=0,max=36)])
    submit = SubmitField('Search')

class MakePlaylistForm(FlaskForm):
    playlist_name = StringField('Playlist', validators=[DataRequired(),Length(min=1,max=36)],render_kw={"placeholder": "Name"})
    submit = SubmitField('Add')
