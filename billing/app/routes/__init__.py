from .provider import get_providers
# from .truck import truck_bp
# from .rate import rate_bp
from .health_check import health_check
# from .bill import bill_bp

def register_blueprints(app):
    app.register_blueprint(get_providers)
    # app.register_blueprint(truck_bp)
    # app.register_blueprint(rate_bp)
    app.register_blueprint(health_check)
    # app.register_blueprint(bill_bp)


