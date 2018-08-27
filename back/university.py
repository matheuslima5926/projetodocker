from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'crud.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)


class University(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    country = db.Column(db.String(80), unique=True)

    def __init__(self, name, country):
        self.name = name
        self.country = country


class UniversitySchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('name', 'country')


university_schema = UniversitySchema()
universities_schema = UniversitySchema(many=True)


# endpoint to create new user
@app.route("/university", methods=["POST"])
def add_university():
    name = request.json['name']
    country = request.json['country']

    new_university = University(name, country)

    db.session.add(new_university)
    db.session.commit()

    return jsonify(new_university)


# endpoint to show all users
@app.route("/university", methods=["GET"])
def get_university():
    all_universities = University.query.all()
    result = universities_schema.dump(all_universities)
    return jsonify(result.data)


# endpoint to get user detail by id
@app.route("/university/<id>", methods=["GET"])
def university_detail(id):
    university = University.query.get(id)
    return university_schema.jsonify(university)


# endpoint to update user
@app.route("/university/<id>", methods=["PUT"])
def university_update(id):
    university = University.query.get(id)
    name = request.json['name']
    country = request.json['country']

    university.name = name
    university.country = country

    db.session.commit()
    return university_schema.jsonify(university)


# endpoint to delete user
@app.route("/university/<id>", methods=["DELETE"])
def university_delete(id):
    university = University.query.get(id)
    db.session.delete(university)
    db.session.commit()

    return university_schema.jsonify(university)


if __name__ == '__main__':
    app.run(debug=True)