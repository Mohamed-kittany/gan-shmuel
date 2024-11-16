# __init__.py
from flask import Flask, jsonify # type: ignore
from app.config import config
from app.extensions import configure_logging
from app.routes import register_blueprints

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    
    # Configure logging
    configure_logging(app)
    
    # Dynamically register all blueprints
    register_blueprints(app)
    
    return app
