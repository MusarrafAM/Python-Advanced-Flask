from flask import Flask, render_template, request
import requests
import smtplib

app = Flask(__name__)

blogs = requests.get("https://api.npoint.io/9c1ffa9b9c1779208bba").json()

my_email = "musapython1@gmail.com"
my_password = "evjmuhullfguaohg"  # this password get from mail  generated


@app.route('/')
def home():
    return render_template("index.html", blogs=blogs)


@app.route('/about')
def get_about():
    return render_template("about.html")


@app.route('/contact', methods=["GET", "POST"])
def get_contact():
    if request.method == "POST":
        name = request.form["name"]
        gmail = request.form["gmail"]
        phone = request.form["phone"]
        text = request.form["text"]

        mail(name, gmail, phone, text)
        return render_template("contact.html", is_successful=True)
    return render_template("contact.html", is_successful=False)


def mail(user_name, e_mail, phone_no, msg):
    email_message = f"Subject:New Message\n\nName: {user_name}\nEmail: {e_mail}\nPhone: {phone_no}\nMessage:{msg}"
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=my_password)
        connection.sendmail(from_addr=my_email,
                            to_addrs=my_email,
                            msg=email_message)

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
