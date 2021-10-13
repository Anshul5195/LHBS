from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from lhbs import db, bcrypt
from lhbs.models import User, Booking
from lhbs.users.forms import (RegistrationForm, LoginForm)


users = Blueprint("users", __name__)


@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('view.home_page'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! Please confirm your email first before log in', 'info')
        return redirect(url_for("users.login"))
    return render_template("register.html", title="Register", form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('view.home_page'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('You are now logged in!', 'success')
            return redirect(url_for('view.home_page'))
        else:
            flash("Login unsuccessful please check email and password", "danger")
    return render_template('login.html', title='Login', form=form)


@login_required
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('view.home_page'))
