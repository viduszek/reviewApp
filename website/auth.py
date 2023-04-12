from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/auth')
def home():
    return "Test-auth"


@auth.route('/auth/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        nick = request.form.get('nick')

        if (email == "") and (nick):
            user = User.query.filter_by(nick=nick).first()
            if user:
                if check_password_hash(user.password, password):
                    flash('Zalogowano pomyślnie. Witaj ' + user.nick + '!', category='success')
                    login_user(user, remember=True)
                    return redirect(url_for('views.home'))
                else:
                    flash('Blad! Podane hasło jest niepoprawne.', category='error')
            else:
                flash('Blad! Taki użytkownik nie występuje w bazie.', category='error')
        elif (email) and (nick == ""):
            user = User.query.filter_by(email=email).first()
            if user:
                if check_password_hash(user.password, password):
                    flash('Zalogowano pomyślnie. Witaj ' + user.nick + '!', category='success')
                    login_user(user, remember=True)
                    return redirect(url_for('views.home'))
                else:
                    flash('Błąd! Podane hasło jest niepoprawne.', category='error')
            else:
                flash('Błąd! Taki użytkownik nie występuje w bazie.', category='error')
        else:
            flash('Podaj albo adres mailowy, albo nazwę użytkownika!', category='error')

    return render_template("login.html", user=current_user)


@auth.route('auth/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        nick = request.form.get('nick')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        email = email.strip()
        password1 = password1.strip()
        password2 = password2.strip()
        nick = nick.strip()

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Blad! Podany email już istnieje w bazie danych.', category='error')
        elif len(email) < 4:
            flash('To nie jest poprawny adres email.', category='error')
        elif len(email) < 2:
            flash('To nie jest poprawny adres email.', category='error')
        elif password1 != password2:
            flash('Hasła się nie zgadzają.', category='error')
        elif len(password1) < 7:
            flash('Twoje hasło jest za krótkie.', category='error')
        else:
            new_user = User(email=email, nick=nick, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Konto zostało utworzone!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign-up.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Wylogowano.', category='warning')
    return redirect(url_for('views.main'))