from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Movies, User, WannaSee
from . import db
from sqlalchemy import select
import json

views = Blueprint('views', __name__)

# query1 = select([Movies.c.user_id, User.c.nick]).select_from(Movies.join(User, Movies.c.user_id == User.c.id))
# q1 = db.session.query([Movies.user_id, User.id]).select_from(Movies, User).join(Movies.user_id == User.id)
# q1 = db.session.query(Movies, User).filter(Movies.user_id == User.id)


@views.route('/', methods=['GET', 'POST'])
def main():
    title = request.form.get('title')
    picture = request.form.get('picture')
    rating = request.form.get('rating')
    streaming = request.form.get('streaming')
    movies = Movies.query.all()

    # usr = Movies.query.filter_by(user_id='user_id').first()

    # usr = Movies.query.get(user)
    # usr = User.query(Movies).join(Movies.user_id == User.id).filter_by(nick=nick)
    # user = User.query.filter_by(email=email).first()

    return render_template("main.html", user=current_user, movies=movies)


@views.route('/my-profile', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        picture = request.form.get('picture')
        rating = request.form.get('rating')
        streamings = request.form.get('streamings')

        if "lastSeen" in request.form:
            title = title.strip()
            description = description.strip()
            if len(picture) < 10:
                picture = 'https://www.mockofun.com/wp-content/uploads/2019/10/movie-poster-credits-178.jpg'
            if len(title) < 2:
                flash("Błąd! Tytuł pozycji nie może być pusty.", category='error')
            if len(description) < 10:
                flash("Błąd! Recenzja jest zbyt krótka (minimum 10 znaków).", category='error')
            else:
                new_mov = Movies(title=title, description=description, picture=picture, rating=rating,
                                 user_id=current_user.id)
                db.session.add(new_mov)
                db.session.commit()
                flash('Recenzja została dodana!', category='success')
        else:
            title = title.strip()
            if len(picture) < 10:
                picture = 'https://www.mockofun.com/wp-content/uploads/2019/10/movie-poster-credits-178.jpg'
            if len(title) < 1:
                flash("Błąd! Tytuł pozycji nie może być pusty.", category='error')
            else:
                new_mov = WannaSee(title=title, streamings=streamings, picture=picture, user_id=current_user.id)
                db.session.add(new_mov)
                db.session.commit()
                flash('Lista do obejrzenia została zaktualizowana!', category='success')
    return render_template("home.html", user=current_user)


@views.route('/delete-movie', methods=['POST'])
def delete_movie():
    movie = json.loads(request.data)
    movID = movie['movID']
    movie = Movies.query.get(movID)

    if movie:
        if movie.user_id == current_user.id:
            db.session.delete(movie)
            db.session.commit()
    return jsonify({})


@views.route('/delete-to-watch', methods=['POST'])
def delete_to_watch():
    movie = json.loads(request.data)
    movID = movie['movID']
    movie = WannaSee.query.get(movID)

    if movie:
        if movie.user_id == current_user.id:
            db.session.delete(movie)
            db.session.commit()
    return jsonify({})
