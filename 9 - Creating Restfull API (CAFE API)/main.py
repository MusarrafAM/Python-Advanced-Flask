from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

from sqlalchemy.exc import NoResultFound

app = Flask(__name__)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    # Change all to dictionary then change it to json. Easy method
    def to_dict(self):
        # # # Method 1.
        # dictionary = {}
        # # Loop through each column in the data record
        # for column in self.__table__.columns:
        #     # Create a new dictionary entry;
        #     # where the key is the name of the column
        #     # and the value is the value of the column
        #     dictionary[column.name] = getattr(self, column.name)
        # return dictionary

        # Method 2. Altenatively use Dictionary Comprehension to do the same thing.
        # -------------------------- VERY IMPORTANT -------------------------------------------
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
        # -------------------------- VERY IMPORTANT -------------------------------------------


@app.route("/")
def home():
    return render_template("index.html")


# But GET is allowed by default on all routes. So no need to specify GET inside methods here.
@app.route('/random')
def get_random_cafe():
    all_cafes = db.session.execute(db.select(Cafe).order_by(Cafe.id)).scalars()
    # --------------List comprehension, doing this in list comprehension will reduce so much stress. -------
    all_cafe_list = [each_cafe for each_cafe in all_cafes]
    random_cafe = random.choice(all_cafe_list)
    print(random_cafe.name)

    # return jsonify(cafe={
    #     "id": random_cafe.id,
    #     "name": random_cafe.name,
    #     "map_url": random_cafe.map_url,
    #     "img_url": random_cafe.img_url,
    #     "location": random_cafe.location,
    #     "seats": random_cafe.seats,
    #     "has_toilet": random_cafe.has_toilet,
    #     "has_wifi": random_cafe.has_wifi,
    #     "has_sockets": random_cafe.has_sockets,
    #     "can_take_calls": random_cafe.can_take_calls,
    #     "coffee_price": random_cafe.coffee_price,
    # })

    # Dict to json method.
    return jsonify(cafe=random_cafe.to_dict())


@app.route("/all")
def get_all_cafes():
    all_cafes = db.session.execute(db.select(Cafe).order_by(Cafe.id)).scalars()
    return jsonify(cafes=[each_cafe.to_dict() for each_cafe in all_cafes])


@app.route('/search')
def search_cafe():
    user_search_loc = request.args.get("loc").title()
    cafe = db.session.execute(db.select(Cafe).filter_by(location=user_search_loc)).scalars()
    if cafe:
        return jsonify(cafes=[cafe.to_dict() for cafe in cafe])
    else:  # If list not empty
        return jsonify(error={"Not Found": "Sorry, We dont have cafe at that location."})


## HTTP GET - Read Record

## HTTP POST - Create Record
@app.route('/add', methods=["POST"])
def add():
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("loc"),
        has_sockets=bool(request.form.get("sockets")),
        has_toilet=bool(request.form.get("toilet")),
        has_wifi=bool(request.form.get("wifi")),
        can_take_calls=bool(request.form.get("calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()

    return jsonify(response={"Success": "Successfully added new cafe"})


# HTTP PUT/PATCH - Update Record

@app.route("/update-price/<cafe_id>", methods=["PATCH"])
def update_price(cafe_id):
    try:
        selected_cafe = db.session.execute(db.select(Cafe).filter_by(id=cafe_id)).scalar_one()
    except NoResultFound:
        # 404 = Resource not found
        return jsonify(Error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404
    else:
        # print(selected_cafe.name)
        # print(selected_cafe.coffee_price)
        selected_cafe.coffee_price = request.args.get("new_price")
        db.session.commit()
        # print(selected_cafe.coffee_price)
        ## Just add the code after the jsonify method. 200 = Ok
        return jsonify(response={"Success": "Successfully price updated"}), 200


## HTTP DELETE - Delete Record

@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def remove_cafe(cafe_id):
    api_key = request.args.get("api-key")
    if api_key == "Musarraf":
        try:
            selected_cafe = db.session.execute(db.select(Cafe).filter_by(id=cafe_id)).scalar_one()
        except NoResultFound:
            # 404 = Resource not found
            return jsonify(Error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404
        else:
            db.session.delete(selected_cafe)
            db.session.commit()
            return jsonify(response={"success": "Successfully deleted the cafe from the database."}), 200
    else:
        return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403


if __name__ == '__main__':
    app.run(debug=True)
