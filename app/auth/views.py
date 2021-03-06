from flask import render_template, redirect, url_for, flash, request
from . import auth
from ..models import User, Subscriber
from .forms import SignUpForm, LoginForm
from .. import db
from flask_login import login_required, login_user, logout_user
from ..email import mail_message

@auth.route('/login', methods = ["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email = login_form.email.data).first()
        if user is not None and user.verify_password(login_form.password.data):
            login_user(user,login_form.remember.data)
            return redirect(request.args.get('next') or url_for('main.index'))

        flash('Invalid username or Password')

    title = "Blog-Town - Log In"

    return render_template('auth/login.html',login_form = login_form,title=title)

@auth.route('/register', methods = ["GET", "POST"])
def register():
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(email = form.email.data, username = form.username.data, password = form.password.data)
        db.session.add(user)
        db.session.commit()

        if form.subscribe.data:
            subscriber = Subscriber(email = form.email.data, username = form.username.data)
            db.session.add(subscriber)
            db.session.commit()

            mail_message("Welcome to Blog-town, where there's a story in everything","email/welcome_user",user.email,user=user)

        return redirect(url_for('auth.login'))
        title = "Blog-Town - New Account"
    return render_template('auth/signup.html', signup_form = form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been Successfully logged out')
    return redirect(url_for("main.index"))