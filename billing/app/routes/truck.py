import logging
from flask import Blueprint, jsonify, request
from ..services import TruckService

WEIGHT_SERVICE_URL = "http://weight-app:6000"


truck_bp = Blueprint('truck', __name__)
truck_service = TruckService()

logger = logging.getLogger(__name__)

@truck_bp.route('/truck', methods=['POST'])
def create_truck():
    """
    registers a truck in the system
    - provider - known provider id
    - id - the truck license plate
    """
    logger.info("Received request to create a new truck.")
    data = request.get_json()
    provider_id = data.get("provider_id")
    truck_id = data.get("id")

    if not truck_id:
        logger.error("Truck id is missing in the request.")
        return jsonify({"error": "Truck id is required"}), 400
    
    if not provider_id:
        logger.error("Provider id is missing in the request.")
        return jsonify({"error": "Provider id is required"}), 400
    
    try:
        truck_service.create_truck(provider_id, truck_id)
        logger.info(f"Truck created successfully")
        return jsonify(), 201
    except ValueError as ve:
        logger.warning(f"Failed to create Truck: {ve}")
        return jsonify({"error": str(ve)}), 409
    except Exception as e:
        logger.error(f"Error creating Truck: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

#PUT /truck/{id} can be used to update provider id
@truck_bp.route('/truck/<id>', methods=['PUT'])
def update_truck(id):
    """
    Updates the id of an existing truck.
    Expects JSON payload: { "id": <str> }
    """
    logger.info(f"Received request to update provider ID with ID: {id}")
    data = request.get_json()
    provider_id = data.get("provider_id")
    
    if not provider_id:
        logger.error("Provider id is missing in the request.")
        return jsonify({"error": "Provider id is required"}), 400

    try:
        truck_service.update_truck(id, provider_id)
        logger.info(f"Truck with ID: {id} updated successfully to provider id: {provider_id}.")
        return jsonify({"message": "Truck updated successfully"}), 200
    except ValueError as ve:
        logger.warning(f"Failed to update truck: {ve}")
        return jsonify({"error": str(ve)}), 404
    except Exception as e:
        if "dosnt exists" in str(e):
            logger.warning(f"This provider ID dose not exist you need to add it first: {provider_id}: {e}")
            return jsonify({"error": "A provider with this id dose not exists."}), 409
        logger.error(f"Error updating truvk with provider id: {provider_id}: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

#truck get
@truck_bp.route("/truck/<id>?from=t1&to=t2", methods=["GET"])
def get_truck_data(id, time_start, time_end):
    """
    Fetches truck data including last known tara and session IDs.

    Query Parameters:
        - id (str): Truck license ID. 404 if non-existent.
        - from (str): Optional start date-time in yyyymmddhhmmss format. Default: 1st of current month at 00:00:00.
        - to (str): Optional end date-time in yyyymmddhhmmss format. Default: current time.

    Returns:
        JSON response:
        {
            "id": <str>,
            "tara": <int>, // last known tara in kg
            "sessions": [<str>, ...] // list of session IDs
        }
    """
    try:
        logger.info(f"Received request to get info about truck: {id}")
        return request.get(f"{WEIGHT_SERVICE_URL}/item/{id}?from={time_start}&to={time_end}"), 200
    except Exception as e:
        logger.error(f"Error geting truck: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500
