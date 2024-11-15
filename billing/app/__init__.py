# __init__.py
from flask import Flask, jsonify # type: ignore
from app.config import config
from app.extensions import configure_logging
# from app.routes.bill import bill_bp
from app.routes.health_check import health_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    
    
    configure_logging(app)
    
    
    #app.register_blueprint(bill_bp, url_prefix='/api')
    app.register_blueprint(health_bp, url_prefix='/api')
    
    return app
