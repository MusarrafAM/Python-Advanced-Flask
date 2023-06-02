from flask import Flask, render_template, redirect
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
bootstrap = Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    url = StringField('Cafe Location on Google Maps (URL)', validators=[DataRequired(), URL()])
    open_time = StringField('Opening Time Eg:- 8AM', validators=[DataRequired()])
    close = StringField('Closing Time Eg:- 5.30PM', validators=[DataRequired()])
    coffe = SelectField('Coffee Rating', choices=['☕', '☕☕', '☕☕☕', '☕☕☕☕', '☕☕☕☕☕'], validators=[DataRequired()])
    wifi = SelectField('Wifi Strength Rating', choices=['✘', '❤', '❤❤', '❤❤❤', '❤❤❤❤', '❤❤❤❤❤'], validators=[DataRequired()])
    power = SelectField('Power Socket Rating', choices=['✘', '🔌', '🔌🔌', ('🔌🔌🔌'), '🔌🔌🔌🔌', '🔌🔌🔌🔌🔌'], validators=[DataRequired()])
    submit = SubmitField('Submit')

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        cafe = form.cafe.data
        url = form.url.data
        open_time = form.open_time.data
        close = form.close.data
        coffe = form.coffe.data
        wifi = form.wifi.data
        power = form.power.data
        final_data = f"\n{cafe},{url},{open_time},{close},{coffe},{wifi},{power}"
        with open("cafe-data.csv", mode="a", encoding="utf8") as file:
            file.write(final_data)
        return redirect("cafes")

    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding="utf8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
