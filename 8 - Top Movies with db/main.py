from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

THE_MOVIE_DB_URL_SEARCH = "https://api.themoviedb.org/3/search/movie"
API_KEY_FOR_THE_MOVIE_DB = "2d2ae7dc5a694e056c5a35bcde04daab"

# create the extension
db = SQLAlchemy()
# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///My_Top_10_Movies.db"
# initialize the app with the extension
db.init_app(app)

app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


# Form
class UpdateForm(FlaskForm):
    rating = StringField('Your rating out of 10', validators=[DataRequired()])
    review = StringField('Your review', validators=[DataRequired()])
    submit = SubmitField("Done")


class AddForm(FlaskForm):
    title = StringField('Movie Title', validators=[DataRequired()])
    submit = SubmitField("Add Movie")


# Database SQLite
class MyMovies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float)
    ranking = db.Column(db.Integer)
    review = db.Column(db.String(250))
    img_url = db.Column(db.String, nullable=False)


with app.app_context():
    db.create_all()

    # new_movie = MyMovies(
    #     title="Phone Booth",
    #     year=2002,
    #     description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
    #     rating=7.3,
    #     ranking=10,
    #     review="My favourite character was the caller.",
    #     img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
    # )
    # db.session.add(new_movie)
    # db.session.commit()


@app.route("/")
def home():
    all_movies = db.session.execute(db.select(MyMovies).order_by(MyMovies.rating)).scalars().all()
    for i in range(len(all_movies)):
        all_movies[i].ranking = len(all_movies) - i
        db.session.commit()
    return render_template("index.html", movies=all_movies)


@app.route("/edit", methods=["POST", "GET"])
def edit():
    form = UpdateForm()
    movie_id = request.args.get('id')
    selected_movie = db.session.execute(db.select(MyMovies).filter_by(id=movie_id)).scalar_one()
    movie_name = selected_movie.title
    if form.validate_on_submit():
        new_rating = float(form.rating.data)
        new_review = form.review.data
        selected_movie.rating = new_rating
        selected_movie.review = new_review
        db.session.commit()

        return redirect("/")

    return render_template("edit.html", form=form, movie=movie_name)


@app.route("/delete")
def delete():
    movie_id = request.args.get('id')
    selected_movie = db.session.execute(db.select(MyMovies).filter_by(id=movie_id)).scalar_one()
    db.session.delete(selected_movie)
    db.session.commit()

    return redirect("/")


@app.route("/add", methods=["POST", "GET"])
def add():
    form = AddForm()
    if form.validate_on_submit():
        movie_name_to_search = form.title.data

        parameters = {
            "api_key": API_KEY_FOR_THE_MOVIE_DB,
            "query": movie_name_to_search,
        }

        data = requests.get(THE_MOVIE_DB_URL_SEARCH, params=parameters).json()["results"]
        return render_template("select.html", options=data)
    return render_template("add.html", form=form)


@app.route("/find")
def find():
    movie_id = request.args.get('id')
    if movie_id:

        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY_FOR_THE_MOVIE_DB}"

        movie_data = requests.get(url).json()

        with app.app_context():
            db.create_all()
            new_movie = MyMovies(
                title=movie_data['title'],
                year=movie_data["release_date"].split('-')[0],
                description=movie_data["overview"],
                img_url="https://image.tmdb.org/t/p/w500" + movie_data["backdrop_path"]
            )
            db.session.add(new_movie)
            db.session.commit()
            selected_movie = db.session.execute(db.select(MyMovies).filter_by(title=movie_data['title'])).scalar_one()
            current_movie_id = selected_movie.id
    return redirect(url_for('edit', id=current_movie_id))


if __name__ == '__main__':
    app.run(debug=True)
