from flask import Flask
#routes inside blueprints
from routes import indexRoute, createRoute, itemRoute, updateRoute, deleteRoute
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

# register the blueprints
# to get access to the routes
app.register_blueprint(indexRoute)
app.register_blueprint(createRoute)
app.register_blueprint(itemRoute)
app.register_blueprint(updateRoute)
app.register_blueprint(deleteRoute)


if __name__ == "__main__":
    app.run(debug=True)