from flask import Flask
import random

app = Flask(__name__)

random_number = random.randint(0, 9)
print(random_number)


@app.route("/")
def home_page():
    return "<h1>Guess a number between 0 and 9</h1>" \
           "<img src = 'https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif'>"


@app.route("/<int:number>")
def number_checker(number):
    if number > random_number:
        return "<h1 style='color:red'>Too high try again!</h1><img src = 'https://media4.giphy.com/media/d4blalI6x2oc4xAA/giphy.gif?cid=ecf05e47q82lva8ocb9knrvkxcja3bxndjvidsf6pri8heo5&rid=giphy.gif&ct=g'>"
    elif number < random_number:
        return "<h1 style='color:blue'>Too low try again!</h1><img src = 'https://media1.giphy.com/media/3NtY188QaxDdC/giphy.gif?cid=ecf05e47worh61f17oohu469o70noou2xujsuiwgz7aeahv6&rid=giphy.gif&ct=g'>"
    else:
        return "<h1 style='color:green'>You found it</h1><img src = 'https://media1.giphy.com/media/Pnb5GTXdF54QxEaiLZ/200w.webp?cid=ecf05e4723i3vi09wl65eoqb75zuw9uu4rttqj6awbj8eiac&rid=200w.webp&ct=g'>"


if __name__ == "__main__":
    app.run(debug=True)
