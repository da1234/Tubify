from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User
from flask_login import current_user, login_user, logout_user
from app import db

@bp.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid password or username")
            return redirect(url_for("auth.login"))
        login_user(user,remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template("login.html",form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user_exists = User.query.filter_by(name=form.username.data).first()
        if user_exists:
            flash("Username is taken!")
            redirect(url_for('auth.register'))
        new_user = User(name=form.username.data,email=form.email.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash("Congrat! you are now registered")
        return redirect(url_for("main.index"))
    return render_template("register.html",form=form)
