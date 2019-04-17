from flask import render_template, request, redirect, url_for
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

@bp.route('/player', methods=['GET','POST'])
@login_required
def player():
    video_id = request.args.get('id',None)
    vid_title = request.args.get('title',None)
    if not video_id:
        return "Peak", 500
    url = request.args.get('url',None)
    results = search_results(vid_title,video_id, url)
    form = MakePlaylistForm()
    if form.validate_on_submit():
        s = Song(title=vid_title,youtube_id=video_id)
        p = Playlist(name=form.playlist_name.data)
        p.songs.append(s)
        current_user.playlists.append(p)
        db.session.add(s)
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template("song_player.html",results=results,form=form)


@bp.route('/new_playlist', methods=['GET','POST'])
@login_required
def new_playlist():
    form = MakePlaylistForm()
    video_id = request.args.get('id',None)
    vid_title = request.args.get('title',None)
    url = request.args.get('url',None)
    print('res',video_id,vid_title,url)
    if form.validate_on_submit():
        s = Song(title=vid_title,youtube_id=video_id)
        p = Playlist(name=form.playlist_name.data)
        p.songs.append(s)
        current_user.playlists.append(p)
        db.session.add(s)
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template("new_playlist.html",form=form,video_id=video_id,vid_title=vid_title,url=url)
