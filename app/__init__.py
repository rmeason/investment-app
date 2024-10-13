from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize the database instance
db = SQLAlchemy()

def create_app():
    # Create a new Flask application instance
    app = Flask(__name__)

    # Load configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../data/sqlite.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database with the app
    db.init_app(app)

    # Import routes and register the blueprint
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
