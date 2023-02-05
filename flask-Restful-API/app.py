"""
Main API-Rest application.
Usage examples:
http://127.0.0.1:5000/parks
http://127.0.0.1:5000/parks?start=1&limit=10
http://127.0.0.1:5000/parks?start=5
http://127.0.0.1:5000/parks?limit=500
http://127.0.0.1:5000/parks?&start_date=2020-01-01&end_date=2020-12-01
http://127.0.0.1:5000/parks?start=1&limit=10&start_date=2020-01-01&end_date=2021-02-01
http://127.0.0.1:5000/Bemmel
http://127.0.0.1:5000/Bemmel?start_date=2020-01-01&end_date=2020-03-01
http://127.0.0.1:5000/Bemmel?start=1&limit=18&start_date=2021-01-01&end_date=2022-02-01
"""


import views
from flask import Flask
from flask_restful import Api


# Create our Flask application
app = Flask(__name__)


# Create our API application
api = Api(app)

# Add resources
api.add_resource(views.ParksListAPI, '/parks')
api.add_resource(views.ParkAPI, '/<string:park>')

app.run(port=5000, debug=True)
