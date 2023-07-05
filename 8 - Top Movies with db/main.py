from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# create the extension
db = SQLAlchemy()
# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books-collection.db"
# initialize the app with the extension
db.init_app(app)


# Create table
class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    all_books = db.session.execute(db.select(Books)).scalars()
    return render_template("index.html", books=all_books)


@app.route('/edit', methods=["POST", "GET"])
def edit():
    if request.method == "POST":
        new_user_rating = request.form.get("rating")
        if new_user_rating == "":
            new_user_rating = 0
        book_id = request.form.get("id")
        selected_book_to_edit = db.session.get(Books, book_id)  # Select by primary key only works for primary key.
        selected_book_to_edit.rating = new_user_rating
        db.session.commit()
        return redirect('/')

    book_id = request.args.get('id')
    selected_book = db.session.execute(db.select(Books).filter_by(id=book_id)).scalar_one()
    return render_template("edit.html", book=selected_book)


@app.route('/delete')
def delete():
    book_id = request.args.get("id")
    selected_book = db.session.execute(db.select(Books).filter_by(id=book_id)).scalar_one()
    db.session.delete(selected_book)
    db.session.commit()

    return redirect("/")


@app.route("/add", methods=["POST", "GET"])
def add():
    if request.method == "POST":
        book_name = request.form.get("name")  # request.form["name"]  Both works the same.
        book_author = request.form.get("author")
        book_rating = request.form.get("rating")
        # Create Record
        new_book = Books(title=book_name, author=book_author, rating=book_rating)
        db.session.add(new_book)
        db.session.commit()

        return redirect('/')  # This and below works the same
        # return redirect(url_for('home'))

    return render_template("add.html")


if __name__ == "__main__":
    app.run(debug=True)
