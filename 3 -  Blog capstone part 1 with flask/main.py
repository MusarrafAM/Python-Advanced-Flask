from flask import Flask, render_template
import requests

app = Flask(__name__)

flake_blogs_api_endpoint = "https://api.npoint.io/c790b4d5cab58020d391"

all_blogs = requests.get(flake_blogs_api_endpoint).json()


@app.route('/')
def home():
    return render_template("index.html", all_blogs=all_blogs)


@app.route("/blog/<int:index>")
def get_blog(index):
    for blog in all_blogs:
        if blog['id'] == index:
            title = blog["title"]
            subtitle = blog["subtitle"]
            body = blog["body"]
    return render_template("post.html", title=title, subtitle=subtitle, body=body)


if __name__ == "__main__":
    app.run(debug=True)


