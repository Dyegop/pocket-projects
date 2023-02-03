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
