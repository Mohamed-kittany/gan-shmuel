import logging
from flask import Blueprint, jsonify
from ..services import health_service


health_bp = Blueprint('health', __name__)
logger = logging.getLogger(__name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    """
    Flask route for the health check.
    Uses the HealthService to determine the application's health status.
    """
    logger.info("Received request for health check.")
    status, http_code = health_service.perform_health_check()
    if http_code == 200:
        logger.info("Health check passed.")
    else:
        logger.error("Health check failed.!!!!!:)")
    return jsonify(status), http_code
