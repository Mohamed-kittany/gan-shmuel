import logging
from flask import Blueprint, request, jsonify
from ..services import rates_service

rates_bp = Blueprint('rates', __name__)
logger = logging.getLogger(__name__)

@rates_bp.route('/', methods=['POST'])
def upload_rates():
    """
    Upload a rates file.
    Uses the RatesService to process and store the rates file.
    """
    logger.info("Received request to upload rates file.")
    file = request.files.get('file')

    if not file:
        logger.error("No file provided in the request.")
        return jsonify({"error": "No file provided"}), 400

    try:
        response = rates_service.process_rates_file(file)
        logger.info("Rates file processed successfully.")
        return jsonify(response), 200
    except ValueError as ve:
        logger.warning(f"Validation error: {ve}")
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        logger.error(f"Failed to process rates file: {e}")
        return jsonify({"error": "Failed to process rates file"}), 500

@rates_bp.route('/', methods=['GET'])
def download_rates():
    """
    Download the rates file.
    Uses the RatesService to fetch the rates file.
    """
    logger.info("Received request to download rates file.")
    try:
        file_path = rates_service.get_rates_file_path()
        if not file_path:
            logger.warning("Rates file not found.")
            return jsonify({"error": "Rates file not found"}), 404

        logger.info("Returning rates file.")
        return rates_service.download_rates_file(file_path)
    except Exception as e:
        logger.error(f"Failed to retrieve rates file: {e}")
        return jsonify({"error": "Failed to retrieve rates file"}), 500

@rates_bp.route('/<int:rate_id>', methods=['PUT'])
def update_rate(rate_id):
    """
    Update a specific rate in the database.
    """
    logger.info(f"Received request to update rate with ID {rate_id}.")
    data = request.json

    if not data or "Rate" not in data:
        logger.error("Invalid or missing data in request.")
        return jsonify({"error": "Invalid or missing data in request"}), 400

    try:
        updated_rate = rates_service.update_rate(rate_id, data)
        if updated_rate:
            logger.info(f"Rate with ID {rate_id} updated successfully.")
            return jsonify(updated_rate), 200
        else:
            logger.warning(f"Rate with ID {rate_id} not found.")
            return jsonify({"error": "Rate not found"}), 404
    except Exception as e:
        logger.error(f"Failed to update rate: {e}")
        return jsonify({"error": "Failed to update rate"}), 500
