# health_check.py
from flask import Blueprint, jsonify, current_app
from app.extensions import get_mysql_connection

health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    try:
        conn = get_mysql_connection()
        conn.cursor().execute("SELECT 1")
        current_app.logger.info("Health check passed: Database connection successful.")
        return jsonify({"status": "OK"}), 200
    except Exception as e:
        current_app.logger.error(f"Health check failed: {e}")
        return jsonify({"status": "Failure"}), 500
