from .health import health_bp
from .provider import provider_bp
from .truck import truck_bp
from .rate import rate_bp
from .bill import billing_bp

def register_blueprints(app):
    """
    Registers all the blueprints with the Flask app and applies a common prefix.
    """
    blueprints = [
        health_bp,
        provider_bp,
        truck_bp,
        rate_bp,
        billing_bp
    ]
    
    for bp in blueprints:
        app.register_blueprint(bp, url_prefix='/api')
