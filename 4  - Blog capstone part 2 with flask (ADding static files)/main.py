from flask import Flask, render_template
import requests

app = Flask(__name__)

blogs = requests.get("https://api.npoint.io/9c1ffa9b9c1779208bba").json()


@app.route('/')
def home():
    return render_template("index.html", blogs=blogs)


@app.route('/about')
def get_about():
    return render_template("about.html")


@app.route('/contact')
def get_contact():
    return render_template("contact.html")


@app.route('/posts/<int:index>')
def get_post(index):
    for blog in blogs:
        if blog["id"] == index:
            title = blog["title"]
            subtitle = blog["subtitle"]
            body = blog["body"]
            author = blog["author"]
            date = blog["date"]
            return render_template("post.html", title=title, subtitle=subtitle, body=body, author=author, date=date)


if __name__ == "__main__":
    app.run(debug=True)
