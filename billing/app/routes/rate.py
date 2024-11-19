import mimetypes
from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
from ..services import RateService
import os

rate_bp = Blueprint('rate', __name__)

ALLOWED_EXTENSIONS = {'xlsx', 'xls', 'csv', 'ods'}

def allowed_file(filename):
    """Check if the file has a valid extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@rate_bp.route('/rates', methods=['GET'])
def get_rates():
    """Retrieve all rates as JSON."""
    try:
        rates = RateService.get_all_rates()
        return jsonify({"rates": rates}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@rate_bp.route('/rates', methods=['POST'])
def upload_rates():
    """Upload and process a rates file."""
    try:
        file = request.files.get('file')
        if not file:
            return jsonify({"error": "No file provided"}), 400

        filename = secure_filename(file.filename)
        if not allowed_file(filename):
            return jsonify({"error": f"File type not allowed. Allowed types are: {', '.join(ALLOWED_EXTENSIONS)}"}), 400

        # Save the uploaded file to a temporary location
        upload_folder = os.path.join(os.getcwd(), "in")
        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)

        # Process and convert file if necessary
        response = RateService.process_and_save_rates(filepath)

        return jsonify(response), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
