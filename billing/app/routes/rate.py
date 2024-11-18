from flask import Blueprint, request, jsonify # type: ignore
from ..services import RateService

rate_bp = Blueprint('rate', __name__, url_prefix='/rates')

@rate_bp.route('/', methods=['POST'])
def upload_rates():
    """Upload and process a rates file."""
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "No file provided"}), 400
    try:
        response = RateService.process_rates_file(file)
        return jsonify(response), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@rate_bp.route('/', methods=['GET'])
def get_all_rates():
    """Retrieve all rates from the database."""
    try:
        rates = RateService.get_all_rates()
        return jsonify(rates), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


