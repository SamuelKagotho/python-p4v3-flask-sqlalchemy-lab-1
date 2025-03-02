# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, request
from flask_migrate import Migrate
import json

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>')
def get_earthquake(id):
    earthquake = Earthquake.query.get(id)
    if earthquake:
        body = {
            "id": earthquake.id,
            "location": earthquake.location,
            "magnitude": earthquake.magnitude,
            "year": earthquake.year
        }
        return make_response(json.dumps(body), 200, {"Content-Type": "application/json"})
    else:
        error_message = {"message": f"Earthquake {id} not found."}
        return make_response(json.dumps(error_message), 404, {"Content-Type": "application/json"})

@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_earthquakes_by_magnitude(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    quakes_list = [{
        "id": quake.id,
        "location": quake.location,
        "magnitude": quake.magnitude,
        "year": quake.year
    } for quake in earthquakes]
    
    response_body = {
        "count": len(quakes_list),
        "quakes": quakes_list
    }
    return make_response(json.dumps(response_body), 200, {"Content-Type": "application/json"})

if __name__ == '__main__':
    app.run(port=5555, debug=True)
