from flask import Blueprint, request, jsonify
from billing.app.services.rate_service import RateService

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

@rate_bp.route('/<product_id>', methods=['GET'])
def get_rate_by_product(product_id):
    """Retrieve a specific rate by product ID."""
    try:
        rate = RateService.get_rate_by_product_id(product_id)
        if rate:
            return jsonify(rate), 200
        else:
            return jsonify({"error": "Rate not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@rate_bp.route('/<product_id>', methods=['PUT'])
def update_rate(product_id):
    """Update a specific rate by product ID."""
    data = request.json
    if not data or "rate" not in data:
        return jsonify({"error": "Invalid or missing data"}), 400
    try:
        updated_rate = RateService.update_rate(product_id, data)
        if updated_rate:
            return jsonify({"message": "Rate updated successfully", "rate": updated_rate}), 200
        else:
            return jsonify({"error": "Rate not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@rate_bp.route('/<product_id>', methods=['DELETE'])
def delete_rate(product_id):
    """Delete a specific rate by product ID."""
    try:
        if RateService.delete_rate(product_id):
            return jsonify({"message": "Rate deleted successfully"}), 200
        else:
            return jsonify({"error": "Rate not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
