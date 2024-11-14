# from .provider import provider_bp
# from .truck import truck_bp
# from .rate import rate_bp
from .health_check import health_check as health_check_bp
# from .bill import bill_bp

def register_blueprints(app):
    # app.register_blueprint(provider_bp)
    # app.register_blueprint(truck_bp)
    # app.register_blueprint(rate_bp)
    app.register_blueprint(health_check_bp)
    # app.register_blueprint(bill_bp)


