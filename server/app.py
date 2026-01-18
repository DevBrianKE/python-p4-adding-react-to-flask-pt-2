#!/usr/bin/env python3

from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from flask_cors import CORS

from models import db, Movie

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)
CORS(app)

@app.route('/movies', methods=['GET'])
def get_movies():
    movies = Movie.query.all()
    return make_response(
        jsonify([movie.to_dict() for movie in movies]),
        200
    )

@app.route('/movies/<int:id>', methods=['PATCH'])
def update_movie(id):
    movie = Movie.query.get(id)

    if not movie:
        return make_response(
            jsonify({"error": "Movie not found"}),
            404
        )

    data = request.get_json()

    if "title" in data:
        movie.title = data["title"]

    db.session.commit()

    return make_response(
        jsonify(movie.to_dict()),
        200
    )

@app.route('/movies/<int:id>', methods=['DELETE'])
def delete_movie(id):
    movie = Movie.query.get(id)

    if not movie:
        return make_response(
            jsonify({"error": "Movie not found"}),
            404
        )

    db.session.delete(movie)
    db.session.commit()

    return make_response("", 204)

@app.route('/')
def home():
    return "Flask backend is running!"

if __name__ == '__main__':
    app.run(port=5555, debug=True)
