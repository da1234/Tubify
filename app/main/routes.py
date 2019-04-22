from flask import render_template, request, redirect, url_for,flash, g
from app.main import bp
from app.main.forms import SearchSongForm, MakePlaylistForm
from flask_login import current_user, login_required
from app.models import Playlist, Song, search_results
from app import db

@bp.route('/', methods=['GET','POST'])
@bp.route('/index', methods=['GET','POST'])
@login_required
def index():
    return render_template("index.html")

@bp.route('/search', methods=['GET','POST'])
@login_required
def search():
    form = SearchSongForm()
    if form.validate_on_submit():
        title = form.songname.data
        results = current_user.search_for_song(title)
        return render_template("search.html",form=form,results=results)
    return render_template("search.html",form=form,results=None)


# TODO: separate out playlist modifiction logic from playing logic
@bp.route('/player', methods=['GET','POST'])
@login_required
def player():
    add = request.args.get('add',None)
    video_id = request.args.get('id',None)
    url = request.args.get('url',None)
    vid_title = request.args.get('title',None)
    results = search_results(vid_title,video_id, url) if video_id else None
    form = MakePlaylistForm()
    current_playlists = current_user.playlists
    s = Song.query.filter_by(title=vid_title).first()
    song_exists = True
    if not s:
        s, song_exists = Song(title=vid_title,youtube_id=video_id), False
    if form.validate_on_submit():
        p = Playlist.query.filter_by(name=form.playlist_name.data,author=current_user).first()
        if p is not None:
            flash('Playlist already exists!', 'error')
            return render_template("song_player.html",results=results,form=form)
        p = Playlist(name=form.playlist_name.data)
        p.songs.append(s)
        current_user.playlists.append(p)
        db.session.add(s)
        db.session.add(p)
        db.session.commit()
        flash("Yay! added new Playlist")
    if request.method == 'POST' and add:
        print("associated: ",results)
        for playlist in current_playlists:
            print(f"{playlist.name}: {request.form.get(playlist.name,False)}")
            if playlist.name in request.form:
                print(f"Adding to : {playlist.name}")
                if not s in playlist.songs:
                    if not song_exists:
                        db.session.add(s)
                    playlist.songs.append(s)
        db.session.commit()

    return render_template("song_player.html",results=results,form=form,
    playlists=current_playlists)

@bp.route('/playlist_player/<name>', methods=['GET','POST'])
@login_required
def playlist_player(name):
    playlist = Playlist.query.filter_by(name=name,author=current_user).first()
    songs = playlist.songs
    return render_template("playlist_player.html",songs=songs)
