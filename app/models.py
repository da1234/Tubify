from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
from time import time
from flask import current_app
from flask_login import UserMixin, current_user
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from collections import namedtuple

playlist_to_song = db.Table('playlist_to_song',
    db.Column('playlist_id',db.Integer,db.ForeignKey('playlist.id'), primary_key=True),
    db.Column('song_id',db.Integer,db.ForeignKey('song.id'), primary_key=True)
    )

search_results = namedtuple('SearchResult',('title','video_id','url'))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(120), index=True)
    password_hash = db.Column(db.String(128))
    playlists = db.relationship('Playlist', backref='author', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash,password)

    def search_for_song(self,songname):
        youtube = build(current_app.config['YOUTUBE_API_SERVICE_NAME'],
         current_app.config['YOUTUBE_API_VERSION'], developerKey=current_app.config['YOUTUBE_API_KEY'])
        search_response = youtube.search().list(q=songname,
            part=current_app.config['YOUTUBE_SEARCH_PART'],
            maxResults=current_app.config['MAX_NO_YOUTUBE_SEARCH_RESULTS'],
            type='video'
        ).execute()

        videos = []

      # Add each result to the appropriate list, and then display the lists of
      # matching videos, channels, and playlists.
        for search_result in search_response.get('items', []):
            if search_result['id']['kind'] == 'youtube#video':
                videos.append(search_results(title=search_result['snippet']['title'],
                                         video_id=search_result['id']['videoId'],url=search_result['snippet']['thumbnails']['default']['url']))

        # print(f"Videos: {videos}")
        return videos


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    youtube_id = db.Column(db.String(64), unique=True)    


class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    songs = db.relationship('Song', secondary=playlist_to_song,
        lazy='subquery', backref=db.backref('playlist',lazy=True))
